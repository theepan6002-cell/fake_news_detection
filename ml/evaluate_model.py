import os
import csv
import json
import joblib

# Import custom pure ML classes for unpickling compatibility
from ml.train_model import (
    PureTfidfVectorizer,
    PureLogisticRegression,
    PureNaiveBayes,
    PureLinearSVM,
    compute_metrics
)

def evaluate_saved_model(test_path="ml/dataset/test_data.csv", model_path="ml/model.pkl", vec_path="ml/vectorizer.pkl"):
    if not os.path.exists(test_path) or not os.path.exists(model_path) or not os.path.exists(vec_path):
        print("Model assets missing. Please run ml/train_model.py first.")
        return None

    X_test = []
    y_test = []
    csv.field_size_limit(262144 * 16)
    with open(test_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            cleaned = row.get("cleaned_content", "").strip()
            label = row.get("label", "").strip()
            if cleaned and label != "":
                X_test.append(cleaned)
                y_test.append(int(label))

    model = joblib.load(model_path)
    vectorizer = joblib.load(vec_path)

    X_vec = vectorizer.transform(X_test)
    preds = model.predict(X_vec)

    metrics = compute_metrics(y_test, preds)

    print("\n" + "="*60)
    print(f"       MODEL EVALUATION REPORT ({getattr(model, 'model_name', 'Trained Model')})")
    print("="*60)
    print(f"Overall Accuracy : {metrics['accuracy'] * 100:.2f}%")
    print(f"Precision        : {metrics['precision'] * 100:.2f}%")
    print(f"Recall           : {metrics['recall'] * 100:.2f}%")
    print(f"F1 Score         : {metrics['f1_score']:.4f}")
    print("-"*60)
    print("Confusion Matrix:")
    cm = metrics["confusion_matrix"]
    print(f"  True Positives  (TP) : {cm['tp']}")
    print(f"  True Negatives  (TN) : {cm['tn']}")
    print(f"  False Positives (FP) : {cm['fp']}")
    print(f"  False Negatives (FN) : {cm['fn']}")
    print("="*60 + "\n")

    return metrics

if __name__ == "__main__":
    evaluate_saved_model()
