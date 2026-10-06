import os
import sys
from flask import Flask, jsonify, send_from_directory, request
from flask_cors import CORS

# Add root directory to python path so ml modules can be loaded smoothly
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from backend.database.db import init_db
from backend.routes.predict import predict_bp
from backend.routes.dashboard import dashboard_bp
from backend.routes.history import history_bp
from backend.routes.dataset import dataset_bp
from backend.routes.model import model_bp
from backend.routes.auth import auth_bp
from backend.routes.admin import admin_bp

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "ai-fake-news-detector-secret-key-2026")
CORS(app)

# Initialize SQLite database
init_db()

# Register API blueprints with /api prefix
app.register_blueprint(predict_bp, url_prefix="/api")
app.register_blueprint(dashboard_bp, url_prefix="/api")
app.register_blueprint(history_bp, url_prefix="/api")
app.register_blueprint(dataset_bp, url_prefix="/api")
app.register_blueprint(model_bp, url_prefix="/api")
app.register_blueprint(auth_bp, url_prefix="/api/auth")
app.register_blueprint(admin_bp, url_prefix="/api/admin")

# Directory containing frontend static files
frontend_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "frontend", "public"))

@app.route("/")
def index():
    if os.path.exists(os.path.join(frontend_dir, "index.html")):
        return send_from_directory(frontend_dir, "index.html")
    return jsonify({
        "status": "online",
        "app": "AI-Powered Fake News Detection & Analytics Engine API",
        "endpoints": [
            "POST /api/predict",
            "GET  /api/dashboard",
            "GET  /api/history",
            "DELETE /api/history/<id>",
            "DELETE /api/history",
            "GET  /api/dataset-stats",
            "GET  /api/model-performance"
        ]
    })

@app.errorhandler(404)
def not_found(e):
    if request.path.startswith("/api/"):
        return jsonify({"error": f"API endpoint '{request.path}' not found."}), 404
        
    # Check if a static file exists (e.g., styles.css, js files)
    rel_path = request.path.lstrip("/")
    if rel_path and os.path.exists(os.path.join(frontend_dir, rel_path)):
        return send_from_directory(frontend_dir, rel_path)
        
    # Fallback to SPA index.html for client-side routing
    if os.path.exists(os.path.join(frontend_dir, "index.html")):
        return send_from_directory(frontend_dir, "index.html")
        
    return jsonify({"error": "Resource not found."}), 404

@app.errorhandler(500)
def server_error(e):
    return jsonify({"error": "Internal server error occurred."}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)

