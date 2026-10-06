import os
import sqlite3
import json
import secrets
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash, check_password_hash

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "database", "fake_news.db")

def get_db_connection():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # 1. Users Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            full_name TEXT NOT NULL,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            role TEXT NOT NULL DEFAULT 'user',
            created_at TEXT NOT NULL,
            avatar TEXT,
            reset_token TEXT,
            reset_token_expires TEXT
        )
    """)

    # 2. Predictions Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS predictions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            news_text TEXT NOT NULL,
            prediction TEXT NOT NULL,
            confidence REAL NOT NULL,
            top_words TEXT,
            timestamp TEXT NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE SET NULL
        )
    """)
    
    # Auto-migrate existing SQLite database if user_id column is missing
    cursor.execute("PRAGMA table_info(predictions)")
    columns = [col["name"] for col in cursor.fetchall()]
    if "user_id" not in columns:
        cursor.execute("ALTER TABLE predictions ADD COLUMN user_id INTEGER")
    conn.commit()

    # Pre-seed default Admin and User if empty
    cursor.execute("SELECT COUNT(*) FROM users")
    user_count = cursor.fetchone()[0]
    
    if user_count == 0:
        now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        admin_pass_hash = generate_password_hash("Admin@123")
        user_pass_hash = generate_password_hash("User@123")

        cursor.executemany("""
            INSERT INTO users (full_name, username, email, password_hash, role, created_at, avatar)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, [
            ("Platform Administrator", "admin", "admin@veritruth.ai", admin_pass_hash, "admin", now_str, "https://api.dicebear.com/7.x/bottts/svg?seed=admin"),
            ("Demo Researcher", "demouser", "user@veritruth.ai", user_pass_hash, "user", now_str, "https://api.dicebear.com/7.x/bottts/svg?seed=demouser")
        ])
        conn.commit()

    # Pre-seed demo predictions if empty
    cursor.execute("SELECT COUNT(*) FROM predictions")
    pred_count = cursor.fetchone()[0]
    if pred_count == 0:
        demo_records = [
            (2, "Federal Reserve announces interest rate stabilization plan amidst market cooling.", "Likely Real", 98.4, '["federal", "reserve", "interest", "rate"]', "2026-08-30 14:22:10"),
            (2, "Secret miracle tea discovered in Amazon rainforest cures all viral infections overnight!", "Likely Fake", 99.1, '["secret", "miracle", "tea", "cures"]', "2026-08-30 16:05:45"),
            (1, "NASA Space Telescope captures high-resolution imagery of newly discovered exoplanet atmosphere.", "Likely Real", 96.8, '["nasa", "telescope", "resolution", "exoplanet"]', "2026-08-31 08:12:30"),
            (1, "Leaked documents reveal alien spacecraft landing in downtown Chicago hidden by government.", "Likely Fake", 97.5, '["leaked", "alien", "spacecraft", "hidden"]', "2026-08-31 09:00:15")
        ]
        cursor.executemany("""
            INSERT INTO predictions (user_id, news_text, prediction, confidence, top_words, timestamp)
            VALUES (?, ?, ?, ?, ?, ?)
        """, demo_records)
        conn.commit()

    conn.close()

# --- User Management Helper Functions ---

def create_user(full_name, username, email, password, role="user"):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Check duplicate
    cursor.execute("SELECT id FROM users WHERE username = ? OR email = ?", (username, email))
    if cursor.fetchone():
        conn.close()
        return None, "Username or email address is already registered."
        
    password_hash = generate_password_hash(password)
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    avatar_url = f"https://api.dicebear.com/7.x/bottts/svg?seed={username}"

    try:
        cursor.execute("""
            INSERT INTO users (full_name, username, email, password_hash, role, created_at, avatar)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (full_name, username, email, password_hash, role, now_str, avatar_url))
        conn.commit()
        new_id = cursor.lastrowid
        conn.close()
        
        return {
            "id": new_id,
            "full_name": full_name,
            "username": username,
            "email": email,
            "role": role,
            "created_at": now_str,
            "avatar": avatar_url
        }, None
    except Exception as e:
        conn.close()
        return None, f"Database error creating user: {str(e)}"

def authenticate_user(identifier, password):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE email = ? OR username = ?", (identifier.lower().strip(), identifier.strip()))
    user = cursor.fetchone()
    conn.close()

    if not user:
        return None, "Invalid email/username or password."

    if check_password_hash(user["password_hash"], password):
        user_dict = {
            "id": user["id"],
            "full_name": user["full_name"],
            "username": user["username"],
            "email": user["email"],
            "role": user["role"],
            "created_at": user["created_at"],
            "avatar": user["avatar"]
        }
        return user_dict, None
    else:
        return None, "Invalid email/username or password."

def get_user_by_id(user_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, full_name, username, email, role, created_at, avatar FROM users WHERE id = ?", (user_id,))
    user = cursor.fetchone()
    conn.close()
    if user:
        return dict(user)
    return None

def update_user_profile(user_id, full_name, email):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Check email duplicate
    cursor.execute("SELECT id FROM users WHERE email = ? AND id != ?", (email, user_id))
    if cursor.fetchone():
        conn.close()
        return None, "Email address is already in use by another account."

    cursor.execute("UPDATE users SET full_name = ?, email = ? WHERE id = ?", (full_name, email, user_id))
    conn.commit()
    conn.close()
    return get_user_by_id(user_id), None

def update_user_password(user_id, old_password, new_password):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT password_hash FROM users WHERE id = ?", (user_id,))
    row = cursor.fetchone()
    
    if not row or not check_password_hash(row["password_hash"], old_password):
        conn.close()
        return False, "Current password does not match."
        
    new_hash = generate_password_hash(new_password)
    cursor.execute("UPDATE users SET password_hash = ? WHERE id = ?", (new_hash, user_id))
    conn.commit()
    conn.close()
    return True, "Password updated successfully."

def create_password_reset_token(email):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, full_name FROM users WHERE email = ?", (email.lower().strip(),))
    user = cursor.fetchone()
    
    if not user:
        conn.close()
        return None, "No account registered with that email address."

    token = secrets.token_urlsafe(32)
    expires = (datetime.now() + timedelta(hours=1)).strftime("%Y-%m-%d %H:%M:%S")

    cursor.execute("UPDATE users SET reset_token = ?, reset_token_expires = ? WHERE id = ?", (token, expires, user["id"]))
    conn.commit()
    conn.close()
    return {"token": token, "email": email, "name": user["full_name"]}, None

def reset_password_with_token(token, new_password):
    conn = get_db_connection()
    cursor = conn.cursor()
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    cursor.execute("SELECT id FROM users WHERE reset_token = ? AND reset_token_expires > ?", (token, now_str))
    user = cursor.fetchone()

    if not user:
        conn.close()
        return False, "Password reset token is invalid or has expired."

    new_hash = generate_password_hash(new_password)
    cursor.execute("UPDATE users SET password_hash = ?, reset_token = NULL, reset_token_expires = NULL WHERE id = ?", (new_hash, user["id"]))
    conn.commit()
    conn.close()
    return True, "Password reset successfully. You may now log in with your new password."

def get_all_users():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT u.id, u.full_name, u.username, u.email, u.role, u.created_at, u.avatar,
               COUNT(p.id) as total_analyzed,
               SUM(CASE WHEN p.prediction = 'Likely Real' THEN 1 ELSE 0 END) as real_count,
               SUM(CASE WHEN p.prediction = 'Likely Fake' THEN 1 ELSE 0 END) as fake_count
        FROM users u
        LEFT JOIN predictions p ON u.id = p.user_id
        GROUP BY u.id
        ORDER BY u.id ASC
    """)
    rows = cursor.fetchall()
    conn.close()
    
    users = []
    for r in rows:
        users.append({
            "id": r["id"],
            "full_name": r["full_name"],
            "username": r["username"],
            "email": r["email"],
            "role": r["role"],
            "created_at": r["created_at"],
            "avatar": r["avatar"],
            "total_analyzed": r["total_analyzed"],
            "real_count": r["real_count"] or 0,
            "fake_count": r["fake_count"] or 0
        })
    return users

def update_user_role(user_id, new_role):
    if new_role not in ["user", "admin"]:
        return False, "Invalid role parameter."
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET role = ? WHERE id = ?", (new_role, user_id))
    conn.commit()
    conn.close()
    return True, "User role updated successfully."

def delete_user_by_id(user_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
    deleted = cursor.rowcount > 0
    conn.commit()
    conn.close()
    return deleted

# --- Prediction Audit Helpers ---

def add_prediction(news_text, prediction, confidence, top_words, user_id=None):
    conn = get_db_connection()
    cursor = conn.cursor()
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    top_words_str = json.dumps(top_words) if isinstance(top_words, list) else str(top_words)
    
    cursor.execute("""
        INSERT INTO predictions (user_id, news_text, prediction, confidence, top_words, timestamp)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (user_id, news_text, prediction, confidence, top_words_str, now_str))
    
    conn.commit()
    new_id = cursor.lastrowid
    conn.close()
    
    return {
        "id": new_id,
        "user_id": user_id,
        "news_text": news_text,
        "prediction": prediction,
        "confidence": confidence,
        "top_words": top_words,
        "timestamp": now_str
    }

def get_history(search=None, filter_type=None, sort_order="newest", user_id=None):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    query = "SELECT * FROM predictions WHERE 1=1"
    params = []
    
    if user_id:
        query += " AND user_id = ?"
        params.append(user_id)
        
    if search:
        query += " AND (news_text LIKE ? OR top_words LIKE ?)"
        params.extend([f"%{search}%", f"%{search}%"])
        
    if filter_type and filter_type.lower() in ["likely real", "likely fake", "real", "fake"]:
        if "real" in filter_type.lower():
            query += " AND prediction = 'Likely Real'"
        else:
            query += " AND prediction = 'Likely Fake'"
            
    if sort_order == "oldest":
        query += " ORDER BY id ASC"
    else:
        query += " ORDER BY id DESC"
        
    cursor.execute(query, params)
    rows = cursor.fetchall()
    conn.close()
    
    history = []
    for r in rows:
        tw = r["top_words"]
        try:
            tw_list = json.loads(tw) if tw else []
        except Exception:
            tw_list = [w.strip() for w in tw.split(",")] if tw else []
            
        history.append({
            "id": r["id"],
            "user_id": r["user_id"],
            "news_text": r["news_text"],
            "prediction": r["prediction"],
            "confidence": float(r["confidence"]),
            "top_words": tw_list,
            "timestamp": r["timestamp"]
        })
    return history

def delete_prediction(prediction_id, user_id=None, is_admin=False):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    if is_admin or user_id is None:
        cursor.execute("DELETE FROM predictions WHERE id = ?", (prediction_id,))
    else:
        cursor.execute("DELETE FROM predictions WHERE id = ? AND user_id = ?", (prediction_id, user_id))
        
    deleted = cursor.rowcount > 0
    conn.commit()
    conn.close()
    return deleted

def clear_all_history(user_id=None, is_admin=False):
    conn = get_db_connection()
    cursor = conn.cursor()
    if is_admin or user_id is None:
        cursor.execute("DELETE FROM predictions")
    else:
        cursor.execute("DELETE FROM predictions WHERE user_id = ?", (user_id,))
    conn.commit()
    conn.close()
    return True

def get_user_prediction_stats(user_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT COUNT(*) FROM predictions WHERE user_id = ?", (user_id,))
    total = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM predictions WHERE user_id = ? AND prediction = 'Likely Real'", (user_id,))
    real_cnt = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM predictions WHERE user_id = ? AND prediction = 'Likely Fake'", (user_id,))
    fake_cnt = cursor.fetchone()[0]
    
    conn.close()
    return {
        "total_analyzed": total,
        "real_count": real_cnt,
        "fake_count": fake_cnt
    }

def get_prediction_counts():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT COUNT(*) FROM predictions")
    total = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM predictions WHERE prediction = 'Likely Real'")
    real_cnt = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM predictions WHERE prediction = 'Likely Fake'")
    fake_cnt = cursor.fetchone()[0]
    
    cursor.execute("""
        SELECT DATE(timestamp) as pred_date, 
               SUM(CASE WHEN prediction = 'Likely Real' THEN 1 ELSE 0 END) as real_c,
               SUM(CASE WHEN prediction = 'Likely Fake' THEN 1 ELSE 0 END) as fake_c,
               COUNT(*) as total_c
        FROM predictions
        GROUP BY DATE(timestamp)
        ORDER BY pred_date ASC
    """)
    timeline_rows = cursor.fetchall()
    timeline = [{"date": r["pred_date"], "real": r["real_c"], "fake": r["fake_c"], "total": r["total_c"]} for r in timeline_rows]
    
    conn.close()
    
    return {
        "total_checked": total,
        "real_count": real_cnt,
        "fake_count": fake_cnt,
        "timeline": timeline
    }
