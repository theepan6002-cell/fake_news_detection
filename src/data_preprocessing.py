import os
import csv
import sys
from utils import clean_text, logger

# Increase CSV field size limit for large articles
csv.field_size_limit(262144 * 16) # 4MB limit per field

def preprocess_datasets(true_path="dataset/True.csv", fake_path="dataset/Fake.csv", output_path="dataset/processed_data.csv"):
    logger.info("Starting data preprocessing...")
    
    if not os.path.exists(true_path) or not os.path.exists(fake_path):
        logger.error(f"Missing source datasets! Looked for '{true_path}' and '{fake_path}'")
        logger.info("Please generate synthetic data first: python src/generate_mock_data.py")
        return False

    records = []
    
    # Load true news (label = 1)
    logger.info(f"Loading true news from {true_path}...")
    try:
        with open(true_path, "r", encoding="utf-8", errors="ignore") as f:
            reader = csv.DictReader(f)
            for row in reader:
                title = row.get("title", "")
                text = row.get("text", "")
                subject = row.get("subject", "")
                date = row.get("date", "")
                
                if title or text:
                    full_content = f"{title} {text}"
                    cleaned = clean_text(full_content)
                    records.append({
                        "title": title,
                        "text": text,
                        "subject": subject,
                        "date": date,
                        "label": 1,
                        "cleaned_content": cleaned
                    })
    except Exception as e:
        logger.error(f"Error reading true news: {e}")
        return False

    # Load fake news (label = 0)
    logger.info(f"Loading fake news from {fake_path}...")
    try:
        with open(fake_path, "r", encoding="utf-8", errors="ignore") as f:
            reader = csv.DictReader(f)
            for row in reader:
                title = row.get("title", "")
                text = row.get("text", "")
                subject = row.get("subject", "")
                date = row.get("date", "")
                
                if title or text:
                    full_content = f"{title} {text}"
                    cleaned = clean_text(full_content)
                    records.append({
                        "title": title,
                        "text": text,
                        "subject": subject,
                        "date": date,
                        "label": 0,
                        "cleaned_content": cleaned
                    })
    except Exception as e:
        logger.error(f"Error reading fake news: {e}")
        return False
        
    logger.info(f"Total merged records: {len(records)}")
    
    # Save processed dataset
    logger.info(f"Saving preprocessed dataset to {output_path}...")
    try:
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, "w", encoding="utf-8", newline="") as f:
            fieldnames = ["title", "text", "subject", "date", "label", "cleaned_content"]
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for record in records:
                writer.writerow(record)
        logger.info("Data preprocessing completed successfully.")
        return True
    except Exception as e:
        logger.error(f"Error writing preprocessed file: {e}")
        return False

if __name__ == "__main__":
    preprocess_datasets()
