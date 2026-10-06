from flask import Blueprint, request, jsonify
from backend.database.db import get_history, delete_prediction, clear_all_history

history_bp = Blueprint("history", __name__)

@history_bp.route("/history", methods=["GET"])
def get_prediction_history():
    search = request.args.get("search", "").strip()
    filter_type = request.args.get("filter", "all").strip()
    sort_order = request.args.get("sort", "newest").strip()
    user_id = request.args.get("user_id")
    is_admin = request.args.get("is_admin") == "true"
    
    # Non-admin users see only their own history
    effective_user_id = None if is_admin else (user_id if user_id else None)
    
    try:
        history = get_history(search=search, filter_type=filter_type, sort_order=sort_order, user_id=effective_user_id)
        return jsonify({
            "count": len(history),
            "history": history
        }), 200
    except Exception as e:
        return jsonify({"error": f"Failed to retrieve history: {str(e)}"}), 500

@history_bp.route("/history/<int:record_id>", methods=["DELETE"])
def delete_record(record_id):
    user_id = request.args.get("user_id")
    is_admin = request.args.get("is_admin") == "true"
    try:
        deleted = delete_prediction(record_id, user_id=user_id, is_admin=is_admin)
        if deleted:
            return jsonify({"message": f"Record {record_id} deleted successfully."}), 200
        else:
            return jsonify({"error": f"Record {record_id} not found or permission denied."}), 404
    except Exception as e:
        return jsonify({"error": f"Failed to delete record: {str(e)}"}), 500

@history_bp.route("/history", methods=["DELETE"])
def clear_history():
    user_id = request.args.get("user_id")
    is_admin = request.args.get("is_admin") == "true"
    try:
        clear_all_history(user_id=user_id, is_admin=is_admin)
        return jsonify({"message": "Prediction history cleared successfully."}), 200
    except Exception as e:
        return jsonify({"error": f"Failed to clear history: {str(e)}"}), 500
