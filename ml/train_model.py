import os
import csv
import json
import math
import random
import joblib
from collections import Counter, defaultdict

class PureTfidfVectorizer:
    def __init__(self, max_features=5000, ngram_range=(1, 2)):
        self.max_features = max_features
        self.ngram_range = ngram_range
        self.vocabulary_ = {}
        self.idf_ = {}
        self.feature_names_ = []

    def _extract_ngrams(self, text):
        if not text or not isinstance(text, str):
            return []
        words = text.split()
        ngrams = []
        n_min, n_max = self.ngram_range
        for n in range(n_min, n_max + 1):
            for i in range(len(words) - n + 1):
                ngrams.append(" ".join(words[i:i+n]))
        return ngrams

    def fit(self, raw_documents):
        term_doc_counts = defaultdict(int)
        global_term_counts = defaultdict(int)
        num_docs = len(raw_documents)

        for doc in raw_documents:
            doc_ngrams = self._extract_ngrams(doc)
            unique_ngrams = set(doc_ngrams)
            for term in unique_ngrams:
                term_doc_counts[term] += 1
            for term in doc_ngrams:
                global_term_counts[term] += 1

        sorted_terms = sorted(global_term_counts.items(), key=lambda x: x[1], reverse=True)
        if self.max_features and len(sorted_terms) > self.max_features:
            selected_terms = [term for term, count in sorted_terms[:self.max_features]]
        else:
            selected_terms = [term for term, count in sorted_terms]

        self.feature_names_ = selected_terms
        self.vocabulary_ = {term: idx for idx, term in enumerate(selected_terms)}

        for term in selected_terms:
            df = term_doc_counts[term]
            self.idf_[term] = math.log((1 + num_docs) / (1 + df)) + 1.0

        return self

    def transform(self, raw_documents):
        sparse_vectors = []
        for doc in raw_documents:
            doc_ngrams = self._extract_ngrams(doc)
            term_freqs = Counter(doc_ngrams)
            vec = {}
            for term, tf in term_freqs.items():
                if term in self.vocabulary_:
                    idx = self.vocabulary_[term]
                    idf = self.idf_[term]
                    vec[idx] = tf * idf

            if vec:
                squared_sum = sum(val**2 for val in vec.values())
                norm = math.sqrt(squared_sum)
                if norm > 0:
                    for idx in vec:
                        vec[idx] /= norm
            sparse_vectors.append(vec)
        return sparse_vectors

    def fit_transform(self, raw_documents):
        return self.fit(raw_documents).transform(raw_documents)


class PureLogisticRegression:
    def __init__(self, lr=0.5, epochs=15, l2_reg=0.0001):
        self.lr = lr
        self.epochs = epochs
        self.l2_reg = l2_reg
        self.weights = {}
        self.bias = 0.0
        self.model_name = "Logistic Regression"

    def fit(self, X, y):
        num_features = max((max(vec.keys()) for vec in X if vec), default=0) + 1
        self.weights = {i: 0.0 for i in range(num_features)}
        self.bias = 0.0

        indices = list(range(len(X)))
        for epoch in range(self.epochs):
            random.shuffle(indices)
            for idx in indices:
                vec = X[idx]
                label = y[idx]

                z = self.bias
                for f_idx, val in vec.items():
                    z += self.weights.get(f_idx, 0.0) * val

                z_clipped = max(-50.0, min(50.0, z))
                p = 1.0 / (1.0 + math.exp(-z_clipped))
                error = label - p

                self.bias += self.lr * error
                for f_idx, val in vec.items():
                    w_val = self.weights.get(f_idx, 0.0)
                    w_val += self.lr * (error * val - self.l2_reg * w_val)
                    self.weights[f_idx] = w_val

    def predict_proba(self, X):
        probs = []
        for vec in X:
            z = self.bias
            for f_idx, val in vec.items():
                z += self.weights.get(f_idx, 0.0) * val
            z_clipped = max(-50.0, min(50.0, z))
            p = 1.0 / (1.0 + math.exp(-z_clipped))
            probs.append([1.0 - p, p])
        return probs

    def predict(self, X):
        probs = self.predict_proba(X)
        return [1 if p[1] >= 0.5 else 0 for p in probs]


class PureNaiveBayes:
    def __init__(self, alpha=1.0):
        self.alpha = alpha
        self.class_log_prior_ = {}
        self.feature_log_prob_ = {}
        self.classes_ = [0, 1]
        self.model_name = "Multinomial Naive Bayes"

    def fit(self, X, y):
        num_docs = len(X)
        num_features = max((max(vec.keys()) for vec in X if vec), default=0) + 1

        doc_counts = Counter(y)
        self.class_log_prior_ = {
            c: math.log(doc_counts[c] / num_docs) for c in self.classes_
        }

        feature_counts = {0: defaultdict(float), 1: defaultdict(float)}
        total_counts = {0: 0.0, 1: 0.0}

        for vec, label in zip(X, y):
            for f_idx, val in vec.items():
                feature_counts[label][f_idx] += val
                total_counts[label] += val

        self.feature_log_prob_ = {0: {}, 1: {}}
        for c in self.classes_:
            denom = total_counts[c] + self.alpha * num_features
            for f_idx in range(num_features):
                count = feature_counts[c].get(f_idx, 0.0)
                self.feature_log_prob_[c][f_idx] = math.log((count + self.alpha) / denom)

    def predict_proba(self, X):
        probs = []
        for vec in X:
            scores = {}
            for c in self.classes_:
                score = self.class_log_prior_[c]
                for f_idx, val in vec.items():
                    log_prob = self.feature_log_prob_[c].get(f_idx, -10.0)
                    score += val * log_prob
                scores[c] = score

            max_score = max(scores.values())
            exp_0 = math.exp(scores[0] - max_score)
            exp_1 = math.exp(scores[1] - max_score)
            denom = exp_0 + exp_1
            probs.append([exp_0 / denom, exp_1 / denom])
        return probs

    def predict(self, X):
        probs = self.predict_proba(X)
        return [1 if p[1] >= 0.5 else 0 for p in probs]


class PureLinearSVM:
    def __init__(self, lr=0.1, epochs=15, C=1.0):
        self.lr = lr
        self.epochs = epochs
        self.C = C
        self.weights = {}
        self.bias = 0.0
        self.model_name = "Linear SVM"

    def fit(self, X, y):
        num_features = max((max(vec.keys()) for vec in X if vec), default=0) + 1
        self.weights = {i: 0.0 for i in range(num_features)}
        self.bias = 0.0

        indices = list(range(len(X)))
        for epoch in range(self.epochs):
            random.shuffle(indices)
            for idx in indices:
                vec = X[idx]
                target = 1.0 if y[idx] == 1 else -1.0

                margin = self.bias
                for f_idx, val in vec.items():
                    margin += self.weights.get(f_idx, 0.0) * val

                if target * margin < 1.0:
                    self.bias += self.lr * self.C * target
                    for f_idx, val in vec.items():
                        w_val = self.weights.get(f_idx, 0.0)
                        w_val = (1.0 - self.lr) * w_val + self.lr * self.C * target * val
                        self.weights[f_idx] = w_val
                else:
                    for f_idx in vec:
                        w_val = self.weights.get(f_idx, 0.0)
                        self.weights[f_idx] = (1.0 - self.lr) * w_val

    def predict_proba(self, X):
        probs = []
        for vec in X:
            z = self.bias
            for f_idx, val in vec.items():
                z += self.weights.get(f_idx, 0.0) * val
            z_clipped = max(-50.0, min(50.0, z * 2.0))
            p = 1.0 / (1.0 + math.exp(-z_clipped))
            probs.append([1.0 - p, p])
        return probs

    def predict(self, X):
        probs = self.predict_proba(X)
        return [1 if p[1] >= 0.5 else 0 for p in probs]


def compute_metrics(y_true, y_pred):
    tp = sum(1 for t, p in zip(y_true, y_pred) if t == 1 and p == 1)
    fp = sum(1 for t, p in zip(y_true, y_pred) if t == 0 and p == 1)
    fn = sum(1 for t, p in zip(y_true, y_pred) if t == 1 and p == 0)
    tn = sum(1 for t, p in zip(y_true, y_pred) if t == 0 and p == 0)

    total = tp + tn + fp + fn
    accuracy = round((tp + tn) / total, 4) if total > 0 else 0.0
    precision = round(tp / (tp + fp), 4) if (tp + fp) > 0 else 0.0
    recall = round(tp / (tp + fn), 4) if (tp + fn) > 0 else 0.0
    f1 = round(2 * precision * recall / (precision + recall), 4) if (precision + recall) > 0 else 0.0

    return {
        "accuracy": accuracy,
        "precision": precision,
        "recall": recall,
        "f1_score": f1,
        "confusion_matrix": {
            "tp": tp,
            "fp": fp,
            "fn": fn,
            "tn": tn
        }
    }


def train_and_compare_models(data_path="ml/dataset/processed_data.csv", model_dir="ml"):
    os.makedirs(model_dir, exist_ok=True)
    os.makedirs(os.path.join(model_dir, "dataset"), exist_ok=True)

    X_texts = []
    y_labels = []

    csv.field_size_limit(262144 * 16)
    with open(data_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            cleaned = row.get("cleaned_content", "").strip()
            label = row.get("label", "").strip()
            if cleaned and label != "":
                X_texts.append(cleaned)
                y_labels.append(int(label))

    # Split train/test (80/20) with fixed seed
    random.seed(42)
    combined = list(zip(X_texts, y_labels))
    random.shuffle(combined)
    split_idx = int(len(combined) * 0.8)

    train_data = combined[:split_idx]
    test_data = combined[split_idx:]

    X_train, y_train = zip(*train_data)
    X_test, y_test = zip(*test_data)

    X_train, X_test = list(X_train), list(X_test)
    y_train, y_test = list(y_train), list(y_test)

    # Save test data CSV
    test_csv = os.path.join(model_dir, "dataset", "test_data.csv")
    with open(test_csv, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["cleaned_content", "label"])
        writer.writeheader()
        for t, l in zip(X_test, y_test):
            writer.writerow({"cleaned_content": t, "label": l})

    # Vectorize
    vectorizer = PureTfidfVectorizer(max_features=5000, ngram_range=(1, 2))
    X_train_vec = vectorizer.fit_transform(X_train)
    X_test_vec = vectorizer.transform(X_test)

    # Instantiate algorithms
    models = {
        "logistic_regression": PureLogisticRegression(lr=0.5, epochs=15),
        "naive_bayes": PureNaiveBayes(alpha=1.0),
        "linear_svm": PureLinearSVM(lr=0.1, epochs=15, C=1.0)
    }

    all_metrics = {}
    best_name = None
    best_f1 = -1.0
    best_model_obj = None

    for name, model in models.items():
        print(f"Training {model.model_name}...")
        model.fit(X_train_vec, y_train)
        preds = model.predict(X_test_vec)
        m = compute_metrics(y_test, preds)
        m["model_name"] = model.model_name
        all_metrics[name] = m

        print(f"[{model.model_name}] Accuracy: {m['accuracy']*100:.2f}%, F1: {m['f1_score']:.4f}")

        if m["f1_score"] > best_f1:
            best_f1 = m["f1_score"]
            best_name = name
            best_model_obj = model

    print(f"\nBest Model Selected: {all_metrics[best_name]['model_name']} with F1 score {best_f1}")

    # Save outputs
    model_pkl = os.path.join(model_dir, "model.pkl")
    vectorizer_pkl = os.path.join(model_dir, "vectorizer.pkl")
    metrics_json = os.path.join(model_dir, "metrics.json")

    joblib.dump(best_model_obj, model_pkl)
    joblib.dump(vectorizer, vectorizer_pkl)

    # Save metrics JSON for API backend
    output_metrics = {
        "best_model": best_name,
        "best_model_display": all_metrics[best_name]["model_name"],
        "comparison": all_metrics,
        "selected_metrics": all_metrics[best_name]
    }

    with open(metrics_json, "w", encoding="utf-8") as f:
        json.dump(output_metrics, f, indent=2)

    # Also sync copy to models/ folder at root for fallback
    os.makedirs("models", exist_ok=True)
    joblib.dump(best_model_obj, "models/fake_news_model.pkl")
    joblib.dump(vectorizer, "models/vectorizer.pkl")

    return output_metrics

if __name__ == "__main__":
    train_and_compare_models()
