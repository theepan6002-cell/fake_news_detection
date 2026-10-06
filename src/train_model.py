import os
import csv
import random
import math
import joblib
from utils import logger
from feature_extraction import fit_transform_tfidf, save_vectorizer

class PureLogisticRegression:
    def __init__(self, lr=0.1, epochs=20, l2_reg=0.0001):
        self.lr = lr
        self.epochs = epochs
        self.l2_reg = l2_reg
        self.weights = {}
        self.bias = 0.0
        
    def fit(self, X, y):
        # Determine vocabulary dimension
        num_features = 0
        for vec in X:
            if vec:
                num_features = max(num_features, max(vec.keys()) + 1)
                
        # Initialize weights
        self.weights = {i: 0.0 for i in range(num_features)}
        self.bias = 0.0
        
        indices = list(range(len(X)))
        logger.info(f"Training PureLogisticRegression for {self.epochs} epochs...")
        
        for epoch in range(self.epochs):
            # Shuffle training data at each epoch
            random.shuffle(indices)
            
            total_loss = 0.0
            for idx in indices:
                vec = X[idx]
                label = y[idx]
                
                # Compute dot product z = bias + w . x
                z = self.bias
                for f_idx, val in vec.items():
                    z += self.weights.get(f_idx, 0.0) * val
                    
                # Sigmoid function
                z = max(-50.0, min(50.0, z)) # Avoid overflow
                p = 1.0 / (1.0 + math.exp(-z))
                
                # Cross-entropy loss for logging
                p_clipped = max(1e-15, min(1 - 1e-15, p))
                loss = - (label * math.log(p_clipped) + (1 - label) * math.log(1 - p_clipped))
                total_loss += loss
                
                # Compute gradient error
                error = label - p
                
                # Update bias
                self.bias += self.lr * error
                
                # Update weights for active sparse elements with L2 regularization
                for f_idx, val in vec.items():
                    w_val = self.weights.get(f_idx, 0.0)
                    w_val += self.lr * (error * val - self.l2_reg * w_val)
                    self.weights[f_idx] = w_val
                    
            avg_loss = total_loss / len(X)
            logger.info(f"Epoch {epoch+1}/{self.epochs} - Loss: {avg_loss:.5f}")
            
    def predict_proba(self, X):
        probs = []
        for vec in X:
            z = self.bias
            for f_idx, val in vec.items():
                z += self.weights.get(f_idx, 0.0) * val
            z = max(-50.0, min(50.0, z))
            p = 1.0 / (1.0 + math.exp(-z))
            probs.append([1.0 - p, p]) # Probability of [0, 1]
        return probs
        
    def predict(self, X):
        probs = self.predict_proba(X)
        return [1 if p[1] >= 0.5 else 0 for p in probs]

class PureLabelEncoder:
    def __init__(self):
        self.classes_ = []
        self.class_to_idx = {}
        self.idx_to_class = {}
        
    def fit(self, y):
        unique_classes = sorted(list(set(y)))
        self.classes_ = unique_classes
        self.class_to_idx = {c: i for i, c in enumerate(unique_classes)}
        self.idx_to_class = {i: c for i, c in enumerate(unique_classes)}
        return self
        
    def transform(self, y):
        return [self.class_to_idx[c] for c in y]
        
    def fit_transform(self, y):
        return self.fit(y).transform(y)
        
    def inverse_transform(self, y_indices):
        return [self.idx_to_class[idx] for idx in y_indices]

def train_test_split_pure(X, y, test_size=0.2, random_seed=42):
    random.seed(random_seed)
    combined = list(zip(X, y))
    random.shuffle(combined)
    split_idx = int(len(combined) * (1 - test_size))
    
    train_set = combined[:split_idx]
    test_set = combined[split_idx:]
    
    X_train, y_train = zip(*train_set) if train_set else ([], [])
    X_test, y_test = zip(*test_set) if test_set else ([], [])
    
    return list(X_train), list(X_test), list(y_train), list(y_test)

def train_fake_news_classifier(data_path="dataset/processed_data.csv", model_path="models/fake_news_model.pkl", encoder_path="models/label_encoder.pkl"):
    logger.info("Starting model training process...")
    
    if not os.path.exists(data_path):
        logger.error(f"Preprocessed data not found at '{data_path}'! Please run preprocessing first.")
        return False
        
    # Read preprocessed records from CSV
    X = []
    y = []
    try:
        # Increase field size limit
        csv.field_size_limit(262144 * 16)
        with open(data_path, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                cleaned_content = row.get("cleaned_content", "")
                label = row.get("label", "")
                if cleaned_content.strip() and label != "":
                    X.append(cleaned_content)
                    y.append(int(label))
    except Exception as e:
        logger.error(f"Error loading processed dataset: {e}")
        return False
        
    logger.info(f"Loaded {len(X)} records for training.")
    
    # Fit label encoder
    logger.info("Fitting LabelEncoder...")
    encoder = PureLabelEncoder()
    # Map: 0 -> Fake, 1 -> True
    y_str = ["True" if val == 1 else "Fake" for val in y]
    y_encoded = encoder.fit_transform(y_str)
    
    # Train-test split
    logger.info("Splitting dataset into train and test sets (80% train, 20% test)...")
    X_train, X_test, y_train, y_test = train_test_split_pure(X, y_encoded, test_size=0.2)
    
    # Save the split test data so evaluate.py can use it
    logger.info("Saving test partition to dataset/test_data.csv...")
    try:
        os.makedirs("dataset", exist_ok=True)
        with open("dataset/test_data.csv", "w", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=["cleaned_content", "label"])
            writer.writeheader()
            for text_item, label_item in zip(X_test, y_test):
                writer.writerow({"cleaned_content": text_item, "label": label_item})
    except Exception as e:
        logger.error(f"Error saving test partition: {e}")
        
    # Feature extraction (TF-IDF Vectorizer) on training data
    X_train_features, vectorizer = fit_transform_tfidf(X_train)
    save_vectorizer(vectorizer)
    
    # Transform test partition to verify features align
    X_train_sparse_features = X_train_features
    
    # Initialize and train classifier
    model = PureLogisticRegression(lr=0.5, epochs=15, l2_reg=0.0001)
    model.fit(X_train_sparse_features, y_train)
    logger.info("Model training completed successfully.")
    
    # Save model and encoder
    os.makedirs(os.path.dirname(model_path), exist_ok=True)
    logger.info(f"Saving model to {model_path}...")
    joblib.dump(model, model_path)
    
    logger.info(f"Saving label encoder to {encoder_path}...")
    joblib.dump(encoder, encoder_path)
    
    logger.info("Model training outputs saved successfully.")
    return True

if __name__ == "__main__":
    train_fake_news_classifier()
