from flask import Blueprint, request, jsonify
from backend.services.inference import analyze_news_text
from backend.database.db import add_prediction

predict_bp = Blueprint("predict", __name__)

@predict_bp.route("/predict", methods=["POST"])
def predict():
    data = request.get_json() or {}
    news_text = data.get("news_text", "").strip()
    
    user_id = data.get("user_id")
    if not news_text:
        return jsonify({"error": "News text cannot be empty."}), 400
        
    try:
        res = analyze_news_text(news_text)
        if "error" in res:
            return jsonify(res), 400
            
        # Store in SQLite database with user_id association
        db_record = add_prediction(
            news_text=res["news_text"],
            prediction=res["prediction"],
            confidence=res["confidence"],
            top_words=res["top_words"],
            user_id=user_id
        )
        res["id"] = db_record["id"]
        res["user_id"] = user_id
        return jsonify(res), 200
    except Exception as e:
        return jsonify({"error": f"An error occurred during classification: {str(e)}"}), 500
