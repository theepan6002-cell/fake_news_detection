import os
import json
from flask import Blueprint, jsonify

model_bp = Blueprint("model", __name__)

METRICS_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "ml", "metrics.json")

@model_bp.route("/model-performance", methods=["GET"])
def get_model_performance():
    try:
        metrics_data = {}
        if os.path.exists(METRICS_PATH):
            with open(METRICS_PATH, "r", encoding="utf-8") as f:
                metrics_data = json.load(f)
                
        pipeline_info = {
            "text_preprocessing": [
                "1. Lowercase conversion",
                "2. URL, HTML tag & Special character removal",
                "3. Tokenization & Punctuation stripping",
                "4. English stop words filtering",
                "5. Stemming / Lemmatization (suffix stripping)",
                "6. Missing values and duplicate record removal"
            ],
            "feature_extraction": {
                "method": "TF-IDF Vectorization",
                "ngram_range": "(1, 2) [Unigrams & Bigrams]",
                "max_features": 5000,
                "norm": "L2 Normalization"
            },
            "algorithms_trained": [
                {"name": "Logistic Regression", "type": "Linear Classifier with L2 Regularization & Sigmoid Link"},
                {"name": "Multinomial Naive Bayes", "type": "Probabilistic Model with Laplace Smoothing"},
                {"name": "Linear SVM", "type": "Support Vector Machine with Hinge Loss & Soft-Margin Optimization"}
            ]
        }
        
        return jsonify({
            "pipeline": pipeline_info,
            "best_model": metrics_data.get("best_model_display", "Logistic Regression"),
            "models_comparison": metrics_data.get("comparison", {}),
            "selected_metrics": metrics_data.get("selected_metrics", {})
        }), 200
    except Exception as e:
        return jsonify({"error": f"Failed to retrieve model performance: {str(e)}"}), 500
