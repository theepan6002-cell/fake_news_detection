import os
import csv
import joblib
from utils import logger
from feature_extraction import load_vectorizer

# Ensure the module can run train_model imports
try:
    from train_model import PureLogisticRegression, PureLabelEncoder
except ImportError:
    pass

def evaluate_model(test_data_path="dataset/test_data.csv", model_path="models/fake_news_model.pkl", vectorizer_path="models/vectorizer.pkl", encoder_path="models/label_encoder.pkl"):
    logger.info("Starting model evaluation...")
    
    if not os.path.exists(test_data_path):
        logger.error(f"Test data file not found at '{test_data_path}'! Please run model training first.")
        return False
        
    if not os.path.exists(model_path) or not os.path.exists(vectorizer_path) or not os.path.exists(encoder_path):
        logger.error("Model assets missing. Please run model training first.")
        return False
        
    # Load dataset using csv DictReader
    X_test_text = []
    y_test = []
    try:
        csv.field_size_limit(262144 * 16)
        with open(test_data_path, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                cleaned = row.get("cleaned_content", "")
                label = row.get("label", "")
                if cleaned.strip() and label != "":
                    X_test_text.append(cleaned)
                    y_test.append(int(label))
    except Exception as e:
        logger.error(f"Error reading test data: {e}")
        return False
        
    if not X_test_text:
        logger.error("Test data is empty or formatted incorrectly.")
        return False
        
    # Load model assets
    model = joblib.load(model_path)
    vectorizer = load_vectorizer(vectorizer_path)
    encoder = joblib.load(encoder_path)
    
    # TF-IDF Feature Extraction
    logger.info("Transforming test data using fitted vectorizer...")
    X_test_features = vectorizer.transform(X_test_text)
    
    # Predict
    logger.info("Running predictions on test set...")
    y_pred = model.predict(X_test_features)
    
    # Calculate metrics in pure Python
    tp = sum(1 for t, p in zip(y_test, y_pred) if t == 1 and p == 1)
    fp = sum(1 for t, p in zip(y_test, y_pred) if t == 0 and p == 1)
    fn = sum(1 for t, p in zip(y_test, y_pred) if t == 1 and p == 0)
    tn = sum(1 for t, p in zip(y_test, y_pred) if t == 0 and p == 0)
    
    total = tp + tn + fp + fn
    accuracy = (tp + tn) / total if total > 0 else 0.0
    
    # Class Fake (0)
    support_fake = tn + fp
    prec_fake = tn / (tn + fn) if (tn + fn) > 0 else 0.0
    rec_fake = tn / (tn + fp) if (tn + fp) > 0 else 0.0
    f1_fake = 2 * prec_fake * rec_fake / (prec_fake + rec_fake) if (prec_fake + rec_fake) > 0 else 0.0
    
    # Class True (1)
    support_true = tp + fn
    prec_true = tp / (tp + fp) if (tp + fp) > 0 else 0.0
    rec_true = tp / (tp + fn) if (tp + fn) > 0 else 0.0
    f1_true = 2 * prec_true * rec_true / (prec_true + rec_true) if (prec_true + rec_true) > 0 else 0.0
    
    print("\n" + "="*60)
    print("                      MODEL EVALUATION REPORT (PURE PYTHON)")
    print("="*60)
    print(f"Overall Accuracy: {accuracy * 100:.2f}%")
    print("-"*60)
    print("Classification Report:")
    print(f"               Precision    Recall      F1-Score    Support")
    print(f"    Fake       {prec_fake:.4f}      {rec_fake:.4f}      {f1_fake:.4f}      {support_fake}")
    print(f"    True       {prec_true:.4f}      {rec_true:.4f}      {f1_true:.4f}      {support_true}")
    print("-"*60)
    print("Confusion Matrix:")
    print(f"                 Predicted Fake    Predicted True")
    print(f"  Actual Fake    {tn:<14d}    {fp:<14d}")
    print(f"  Actual True    {fn:<14d}    {tp:<14d}")
    print("="*60 + "\n")
    
    logger.info("Model evaluation completed.")
    return True

if __name__ == "__main__":
    evaluate_model()
