import os
import sys
from functools import wraps
from flask import Flask, render_template, request, jsonify, session, redirect, url_for

# Add the parent directory to the python path to import src modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

try:
    from src.predict import predict_news
    from src.utils import logger
except ImportError:
    # Fallback if executing directly or from wrong directory
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))
    from predict import predict_news
    from utils import logger

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "truthengine-fake-news-detection-secret-key-2026")

# Ensure required assets exist or show warning (resolve paths relative to project root)
base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
model_paths = {
    "model": os.path.join(base_dir, "models", "fake_news_model.pkl"),
    "vectorizer": os.path.join(base_dir, "models", "vectorizer.pkl"),
    "encoder": os.path.join(base_dir, "models", "label_encoder.pkl"),
}

assets_exist = (
    os.path.exists(model_paths["model"]) and
    os.path.exists(model_paths["vectorizer"]) and
    os.path.exists(model_paths["encoder"]) 
)

if not assets_exist:
    logger.warning("="*80)
    logger.warning(f"WARNING: Prediction assets not found at expected locations: {model_paths}")
    logger.warning("The application will fail on predictions until you train or place the model assets in 'models/' at project root:")
    logger.warning("  1. Run 'python src/generate_mock_data.py' from project root")
    logger.warning("  2. Run 'python src/data_preprocessing.py' from project root")
    logger.warning("  3. Run 'python src/train_model.py' from project root")
    logger.warning("="*80)

# Demo user credentials (in production, use a proper database)
DEMO_USERS = {
    "admin": "password123",
    "user": "user123",
    "test": "test123"
}

# Login required decorator
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "user" not in session:
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return decorated_function

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "").strip()
        remember = request.form.get("remember") == "on"
        
        if not username or not password:
            return render_template("login.html", error="Username and password are required.")
        
        if username in DEMO_USERS and DEMO_USERS[username] == password:
            session["user"] = username
            session.permanent = remember
            return redirect(url_for("index"))
        else:
            return render_template("login.html", error="Invalid username or password.")
    
    if "user" in session:
        return redirect(url_for("index"))
    
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

@app.route("/")
@login_required
def index():
    return render_template("index.html", user=session.get("user"))

@app.route("/about")
@login_required
def about():
    return render_template("about.html", user=session.get("user"))

@app.route("/predict", methods=["POST"])
@login_required
def predict():
    news_text = request.form.get("news_text", "").strip()
    if not news_text:
        return render_template("index.html", error="Please enter some news text to analyze.", user=session.get("user"))
        
    try:
        result = predict_news(news_text)
        if "error" in result:
            return render_template("index.html", error=result["error"], user=session.get("user"))
        return render_template("result.html", result=result, user=session.get("user"))
    except Exception as e:
        logger.error(f"Prediction error: {e}")
        return render_template("index.html", error=f"An error occurred during prediction: {str(e)}", user=session.get("user"))

@app.route("/api/predict", methods=["POST"])
@login_required
def api_predict():
    data = request.get_json() or {}
    news_text = data.get("news_text", "").strip()
    
    if not news_text:
        return jsonify({"error": "No news text provided."}), 400
        
    try:
        result = predict_news(news_text)
        if "error" in result:
            return jsonify({"error": result["error"]}), 400
        return jsonify(result)
    except Exception as e:
        logger.error(f"API prediction error: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=5000)
