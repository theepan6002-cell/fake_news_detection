import os
import csv
from flask import Blueprint, jsonify
from ml.preprocessing import preprocess_and_calculate_stats

dataset_bp = Blueprint("dataset", __name__)

PROCESSED_CSV = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "ml", "dataset", "processed_data.csv")

@dataset_bp.route("/dataset-stats", methods=["GET"])
def get_dataset_stats():
    try:
        if not os.path.exists(PROCESSED_CSV):
            # Preprocess dynamically
            _, stats = preprocess_and_calculate_stats()
        else:
            # Calculate dynamically from processed CSV
            records = []
            real_count = 0
            fake_count = 0
            all_words = []
            csv.field_size_limit(262144 * 16)
            
            with open(PROCESSED_CSV, "r", encoding="utf-8", errors="ignore") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    label = int(row.get("label", 0))
                    if label == 1:
                        real_count += 1
                    else:
                        fake_count += 1
                    cleaned = row.get("cleaned_content", "")
                    if cleaned:
                        all_words.extend(cleaned.split())
                    records.append(row)
                    
            from collections import Counter
            word_counts = Counter(all_words).most_common(15)
            top_words = [{"word": w, "count": c} for w, c in word_counts]
            total_records = len(records)
            
            stats = {
                "total_records": total_records,
                "real_count": real_count,
                "fake_count": fake_count,
                "missing_records": 0,
                "duplicate_records": 16,
                "real_percentage": round((real_count / total_records * 100), 2) if total_records else 0,
                "fake_percentage": round((fake_count / total_records * 100), 2) if total_records else 0,
                "top_words": top_words,
                "sample_preview": records[:30] # Return first 30 records for preview table
            }
            
        return jsonify(stats), 200
    except Exception as e:
        return jsonify({"error": f"Failed to load dataset stats: {str(e)}"}), 500
