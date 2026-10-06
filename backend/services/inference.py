import os
import sys
import joblib
from datetime import datetime
from ml.preprocessing import clean_text
import ml.train_model
from ml.train_model import (
    PureTfidfVectorizer,
    PureLogisticRegression,
    PureNaiveBayes,
    PureLinearSVM
)

# Bind custom ML classes to __main__ module to fix joblib unpickling namespace lookups
main_mod = sys.modules.get("__main__")
if main_mod:
    setattr(main_mod, "PureLogisticRegression", PureLogisticRegression)
    setattr(main_mod, "PureNaiveBayes", PureNaiveBayes)
    setattr(main_mod, "PureLinearSVM", PureLinearSVM)
    setattr(main_mod, "PureTfidfVectorizer", PureTfidfVectorizer)

MODEL_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "ml", "model.pkl")
VEC_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "ml", "vectorizer.pkl")

# Fallback paths
if not os.path.exists(MODEL_PATH):
    MODEL_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "models", "fake_news_model.pkl")
if not os.path.exists(VEC_PATH):
    VEC_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "models", "vectorizer.pkl")

_model = None
_vectorizer = None

def load_ml_assets():
    global _model, _vectorizer
    if _model is None:
        if os.path.exists(MODEL_PATH):
            _model = joblib.load(MODEL_PATH)
        else:
            raise FileNotFoundError(f"Model file not found at {MODEL_PATH}. Please train the model first.")
            
    if _vectorizer is None:
        if os.path.exists(VEC_PATH):
            _vectorizer = joblib.load(VEC_PATH)
        else:
            raise FileNotFoundError(f"Vectorizer file not found at {VEC_PATH}. Please train the model first.")
            
    return _model, _vectorizer

def analyze_news_text(news_text):
    if not news_text or not isinstance(news_text, str) or not news_text.strip():
        return {"error": "Please provide valid news text for analysis."}
        
    cleaned = clean_text(news_text)
    if not cleaned:
        return {"error": "Input text contains only stop words or special characters. Please provide meaningful content."}
        
    model, vectorizer = load_ml_assets()
    
    # Transform text
    vecs = vectorizer.transform([cleaned])
    vec = vecs[0]
    
    # Predict probabilities
    probs = model.predict_proba(vecs)[0]
    prob_fake, prob_real = probs[0], probs[1]
    
    label = "Likely Real" if prob_real >= prob_fake else "Likely Fake"
    confidence = round(max(prob_real, prob_fake) * 100, 2)
    
    # Extract top word signals
    top_words = []
    if vec:
        # Sort feature indices by TF-IDF weight
        sorted_indices = sorted(vec.items(), key=lambda x: x[1], reverse=True)[:5]
        idx_to_word = {idx: term for term, idx in vectorizer.vocabulary_.items()}
        top_words = [idx_to_word[idx] for idx, val in sorted_indices if idx in idx_to_word]
        
    explanation = (
        f"This article was classified as '{label}' with {confidence}% model confidence. "
        "Predictions are generated using TF-IDF feature extraction and trained Machine Learning models. "
        "Always cross-reference critical news with verified journalistic sources."
    )
    
    return {
        "news_text": news_text,
        "prediction": label,
        "confidence": confidence,
        "probabilities": {
            "real": round(prob_real * 100, 2),
            "fake": round(prob_fake * 100, 2)
        },
        "top_words": top_words,
        "cleaned_text": cleaned,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "explanation": explanation
    }
