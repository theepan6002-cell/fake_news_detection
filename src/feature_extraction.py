import os
import joblib
import math
from collections import Counter, defaultdict
from utils import logger

class PureTfidfVectorizer:
    def __init__(self, max_features=5000, ngram_range=(1, 2)):
        self.max_features = max_features
        self.ngram_range = ngram_range
        self.vocabulary_ = {} # Term to index mapping
        self.idf_ = {}        # Term to IDF score mapping
        
    def _extract_ngrams(self, text):
        if not text or not isinstance(text, str):
            return []
        words = text.split()
        ngrams = []
        n_min, n_max = self.ngram_range
        for n in range(n_min, n_max + 1):
            for i in range(len(words) - n + 1):
                ngram = " ".join(words[i:i+n])
                ngrams.append(ngram)
        return ngrams
        
    def fit(self, raw_documents):
        term_doc_counts = defaultdict(int)
        global_term_counts = defaultdict(int)
        num_docs = len(raw_documents)
        
        logger.info(f"Extracting n-grams and calculating frequencies for {num_docs} documents...")
        for doc in raw_documents:
            doc_ngrams = self._extract_ngrams(doc)
            unique_ngrams = set(doc_ngrams)
            for term in unique_ngrams:
                term_doc_counts[term] += 1
            for term in doc_ngrams:
                global_term_counts[term] += 1
                
        # Sort terms by frequency and slice to max_features
        logger.info("Sorting terms by frequency...")
        sorted_terms = sorted(global_term_counts.items(), key=lambda x: x[1], reverse=True)
        if self.max_features and len(sorted_terms) > self.max_features:
            selected_terms = [term for term, count in sorted_terms[:self.max_features]]
        else:
            selected_terms = [term for term, count in sorted_terms]
            
        # Build vocabulary dictionary
        self.vocabulary_ = {term: idx for idx, term in enumerate(selected_terms)}
        
        # Calculate smoothed IDF: log((1 + N) / (1 + df)) + 1
        logger.info("Calculating IDF scores...")
        for term in selected_terms:
            df = term_doc_counts[term]
            self.idf_[term] = math.log((1 + num_docs) / (1 + df)) + 1
            
        logger.info(f"Vectorizer fitted successfully with {len(self.vocabulary_)} features.")
        return self
        
    def transform(self, raw_documents):
        # Returns a list of dicts: each dict maps term_index -> tfidf_value
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
                    
            # Apply L2 Normalization
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

def fit_transform_tfidf(texts, max_features=5000, ngrams=(1, 2)):
    vectorizer = PureTfidfVectorizer(max_features=max_features, ngram_range=ngrams)
    features = vectorizer.fit_transform(texts)
    return features, vectorizer

def save_vectorizer(vectorizer, filepath="models/vectorizer.pkl"):
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    logger.info(f"Saving pure-python vectorizer to {filepath}...")
    joblib.dump(vectorizer, filepath)
    logger.info("Vectorizer saved successfully.")

def load_vectorizer(filepath="models/vectorizer.pkl"):
    if not os.path.exists(filepath):
        logger.error(f"Vectorizer file not found: {filepath}")
        raise FileNotFoundError(f"Vectorizer file not found: {filepath}")
    logger.info(f"Loading pure-python vectorizer from {filepath}...")
    return joblib.load(filepath)
