import os
import re
import csv
import string
from collections import Counter

# Standard English Stop Words list
STOP_WORDS = set([
    "a", "about", "above", "after", "again", "against", "all", "am", "an", "and", "any", "are", "aren't",
    "as", "at", "be", "because", "been", "before", "being", "below", "between", "both", "but", "by",
    "can't", "cannot", "could", "couldn't", "did", "didn't", "do", "does", "doesn't", "doing", "don't",
    "down", "during", "each", "few", "for", "from", "further", "had", "hadn't", "has", "hasn't", "have",
    "haven't", "having", "he", "he'd", "he'll", "he's", "her", "here", "here's", "hers", "herself",
    "him", "himself", "his", "how", "how's", "i", "i'd", "i'll", "i'm", "i've", "if", "in", "into",
    "is", "isn't", "it", "it's", "its", "itself", "let's", "me", "more", "most", "mustn't", "my",
    "myself", "no", "nor", "not", "of", "off", "on", "once", "only", "or", "other", "ought", "our",
    "ours", "ourselves", "out", "over", "own", "same", "shan't", "she", "she'd", "she'll", "she's",
    "should", "shouldn't", "so", "some", "such", "than", "that", "that's", "the", "their", "theirs",
    "them", "themselves", "then", "there", "there's", "these", "they", "they'd", "they'll", "they're",
    "they've", "this", "those", "through", "to", "too", "under", "until", "up", "very", "was", "wasn't",
    "we", "we'd", "we'll", "we're", "we've", "were", "weren't", "what", "what's", "when", "when's",
    "where", "where's", "which", "while", "who", "who's", "whom", "why", "why's", "with", "won't",
    "would", "wouldn't", "you", "you'd", "you'll", "you're", "you've", "your", "yours", "yourself",
    "yourselves", "said", "reuters", "washington", "say", "says", "also", "would", "one", "two", "new"
])

def clean_text(text):
    """
    Data Preprocessing Pipeline:
    1. Lowercase conversion
    2. Special character & URL removal
    3. Punctuation removal
    4. Tokenization
    5. Stop words removal
    6. Basic Stemming/Lemmatization (suffix stripping)
    """
    if not text or not isinstance(text, str):
        return ""
        
    # 1. Lowercase
    text = text.lower()
    
    # 2. Remove URLs, HTML tags, emails
    text = re.sub(r'https?://\S+|www\.\S+', '', text)
    text = re.sub(r'<.*?>', '', text)
    text = re.sub(r'\S+@\S+', '', text)
    
    # 3. Remove punctuation & special characters / digits
    text = re.sub(r'[^a-z\s]', ' ', text)
    
    # 4. Tokenization
    tokens = text.split()
    
    # 5. Stop words removal & 6. Stemming (Suffix reduction)
    cleaned_tokens = []
    for token in tokens:
        if token not in STOP_WORDS and len(token) > 2:
            # Simple rules-based lemmatizer/stemmer
            if token.endswith("ing") and len(token) > 5:
                token = token[:-3]
            elif token.endswith("ed") and len(token) > 4:
                token = token[:-2]
            elif token.endswith("ly") and len(token) > 4:
                token = token[:-2]
            elif token.endswith("es") and len(token) > 4:
                token = token[:-2]
            elif token.endswith("s") and not token.endswith("ss") and len(token) > 3:
                token = token[:-1]
            cleaned_tokens.append(token)
            
    return " ".join(cleaned_tokens)

def preprocess_and_calculate_stats(true_csv_path="dataset/True.csv", fake_csv_path="dataset/Fake.csv", output_csv_path="ml/dataset/processed_data.csv"):
    """
    Reads datasets, handles missing values & duplicates, performs preprocessing,
    and returns dynamic dataset statistics.
    """
    csv.field_size_limit(262144 * 16)
    
    records = []
    missing_count = 0
    seen_texts = set()
    duplicate_count = 0
    real_count = 0
    fake_count = 0
    all_words = []
    
    # Load True News
    if os.path.exists(true_csv_path):
        with open(true_csv_path, "r", encoding="utf-8", errors="ignore") as f:
            reader = csv.DictReader(f)
            for row in reader:
                title = (row.get("title") or "").strip()
                text = (row.get("text") or "").strip()
                subject = (row.get("subject") or "general").strip()
                date = (row.get("date") or "").strip()
                
                if not title and not text:
                    missing_count += 1
                    continue
                    
                full_raw = f"{title} {text}".strip()
                if full_raw in seen_texts:
                    duplicate_count += 1
                    continue
                seen_texts.add(full_raw)
                
                cleaned = clean_text(full_raw)
                if not cleaned:
                    missing_count += 1
                    continue
                    
                real_count += 1
                all_words.extend(cleaned.split())
                records.append({
                    "title": title,
                    "text": text,
                    "subject": subject,
                    "date": date,
                    "label": 1, # 1 = Real
                    "label_name": "Likely Real",
                    "cleaned_content": cleaned
                })
                
    # Load Fake News
    if os.path.exists(fake_csv_path):
        with open(fake_csv_path, "r", encoding="utf-8", errors="ignore") as f:
            reader = csv.DictReader(f)
            for row in reader:
                title = (row.get("title") or "").strip()
                text = (row.get("text") or "").strip()
                subject = (row.get("subject") or "news").strip()
                date = (row.get("date") or "").strip()
                
                if not title and not text:
                    missing_count += 1
                    continue
                    
                full_raw = f"{title} {text}".strip()
                if full_raw in seen_texts:
                    duplicate_count += 1
                    continue
                seen_texts.add(full_raw)
                
                cleaned = clean_text(full_raw)
                if not cleaned:
                    missing_count += 1
                    continue
                    
                fake_count += 1
                all_words.extend(cleaned.split())
                records.append({
                    "title": title,
                    "text": text,
                    "subject": subject,
                    "date": date,
                    "label": 0, # 0 = Fake
                    "label_name": "Likely Fake",
                    "cleaned_content": cleaned
                })

    # Save output CSV
    os.makedirs(os.path.dirname(output_csv_path), exist_ok=True)
    with open(output_csv_path, "w", encoding="utf-8", newline="") as f:
        fieldnames = ["title", "text", "subject", "date", "label", "label_name", "cleaned_content"]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for r in records:
            writer.writerow(r)
            
    word_counts = Counter(all_words).most_common(20)
    top_words = [{"word": w, "count": c} for w, c in word_counts]
    
    total_records = len(records)
    stats = {
        "total_records": total_records,
        "real_count": real_count,
        "fake_count": fake_count,
        "missing_records": missing_count,
        "duplicate_records": duplicate_count,
        "real_percentage": round((real_count / total_records * 100), 2) if total_records else 0,
        "fake_percentage": round((fake_count / total_records * 100), 2) if total_records else 0,
        "top_words": top_words
    }
    
    return records, stats

if __name__ == "__main__":
    records, stats = preprocess_and_calculate_stats()
    print(f"Preprocessed {stats['total_records']} records successfully.")
    print(f"Real: {stats['real_count']}, Fake: {stats['fake_count']}, Duplicates: {stats['duplicate_records']}")
