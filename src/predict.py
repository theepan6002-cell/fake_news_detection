import os
import sys
import argparse
import joblib
from utils import clean_text, logger
from feature_extraction import load_vectorizer

# Ensure the class definitions are available in the module scope for joblib unpickling
try:
    from train_model import PureLogisticRegression, PureLabelEncoder
    from feature_extraction import PureTfidfVectorizer
except ImportError:
    from src.train_model import PureLogisticRegression, PureLabelEncoder
    from src.feature_extraction import PureTfidfVectorizer

# Bind classes to __main__ to ensure joblib unpickling succeeds
main_module = sys.modules.get('__main__')
if main_module:
    if not hasattr(main_module, 'PureLogisticRegression'):
        main_module.PureLogisticRegression = PureLogisticRegression
    if not hasattr(main_module, 'PureLabelEncoder'):
        main_module.PureLabelEncoder = PureLabelEncoder
    if not hasattr(main_module, 'PureTfidfVectorizer'):
        main_module.PureTfidfVectorizer = PureTfidfVectorizer

# Global variables to cache loaded models
_model = None
_vectorizer = None
_encoder = None

def load_prediction_assets(model_path=None, vectorizer_path=None, encoder_path=None):
    global _model, _vectorizer, _encoder
    
    if _model is not None and _vectorizer is not None and _encoder is not None:
        return _model, _vectorizer, _encoder
        
    # Resolve default asset paths relative to project root (parent of src)
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    if model_path is None:
        model_path = os.path.join(base_dir, "models", "fake_news_model.pkl")
    if vectorizer_path is None:
        vectorizer_path = os.path.join(base_dir, "models", "vectorizer.pkl")
    if encoder_path is None:
        encoder_path = os.path.join(base_dir, "models", "label_encoder.pkl")

    if not os.path.exists(model_path) or not os.path.exists(vectorizer_path) or not os.path.exists(encoder_path):
        raise FileNotFoundError(
            f"Prediction assets missing! Expected files:\n  model: {model_path}\n  vectorizer: {vectorizer_path}\n  encoder: {encoder_path}\nPlease run model training first (python src/train_model.py from project root)"
        )
        
    logger.info("Loading prediction assets...")
    _model = joblib.load(model_path)
    _vectorizer = load_vectorizer(vectorizer_path)
    _encoder = joblib.load(encoder_path)
    logger.info("Prediction assets loaded successfully.")
    
    return _model, _vectorizer, _encoder

def predict_news(text: str):
    """
    Predicts whether a given news text is True or Fake.
    Returns:
        dict: {'prediction': 'True'|'Fake', 'confidence': float, 'raw_text': str}
    """
    model, vectorizer, encoder = load_prediction_assets()
    
    # 1. Clean the input text
    cleaned = clean_text(text)
    if not cleaned.strip():
        return {
            "prediction": "Unknown",
            "confidence": 0.0,
            "error": "The input text contained no meaningful words after preprocessing."
        }
        
    # 2. Extract features
    features = vectorizer.transform([cleaned])
    
    # 3. Predict probability and class
    prob = model.predict_proba(features)[0]
    pred_class_idx = model.predict(features)[0]
    
    # 4. Decode label
    pred_label = encoder.inverse_transform([pred_class_idx])[0]
    
    # Class confidence mapping
    confidence = float(prob[pred_class_idx])
    
    return {
        "prediction": pred_label,
        "confidence": confidence,
        "raw_text": text
    }

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Predict whether a news article is True/Credible or Fake.")
    parser.add_argument("--text", type=str, help="The full body text of the news article to analyze.")
    args = parser.parse_args()
    
    # If no text is provided, prompt the user
    text = args.text
    if not text:
        logger.info("No text provided via command line. Please enter the article text below:")
        try:
            text = input("News Text: ")
        except (KeyboardInterrupt, EOFError):
            print("\nExiting prediction CLI.")
            exit(0)
            
    if not text.strip():
        logger.error("Input text cannot be empty.")
        exit(1)
        
    try:
        result = predict_news(text)
        print("\n" + "="*50)
        print("                 PREDICTION RESULT")
        print("="*50)
        print(f"Classification : {result['prediction']}")
        print(f"Confidence     : {result['confidence'] * 100:.2f}%")
        print("="*50 + "\n")
    except Exception as e:
        logger.error(f"Prediction failed: {e}")
        exit(1)
