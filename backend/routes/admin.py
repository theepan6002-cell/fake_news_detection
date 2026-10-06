# pyrefly: ignore [missing-import]
from flask import Blueprint, request, jsonify
from backend.database.db import (
    get_all_users,
    update_user_role,
    delete_user_by_id,
    get_prediction_counts
)

admin_bp = Blueprint("admin", __name__)

@admin_bp.route("/stats", methods=["GET"])
def get_admin_stats():
    try:
        users = get_all_users()
        pred_stats = get_prediction_counts()
        
        admin_count = sum(1 for u in users if u["role"] == "admin")
        user_count = sum(1 for u in users if u["role"] == "user")
        
        return jsonify({
            "total_users": len(users),
            "admin_count": admin_count,
            "user_count": user_count,
            "prediction_stats": pred_stats
        }), 200
    except Exception as e:
        return jsonify({"error": f"Failed to retrieve admin stats: {str(e)}"}), 500

@admin_bp.route("/users", methods=["GET"])
def list_users():
    try:
        users = get_all_users()
        return jsonify({
            "count": len(users),
            "users": users
        }), 200
    except Exception as e:
        return jsonify({"error": f"Failed to list users: {str(e)}"}), 500

@admin_bp.route("/users/<int:user_id>/role", methods=["PUT"])
def change_role(user_id):
    data = request.get_json() or {}
    new_role = data.get("role", "").strip().lower()
    
    if not new_role:
        return jsonify({"error": "Role parameter is required."}), 400
        
    success, msg = update_user_role(user_id, new_role)
    if not success:
        return jsonify({"error": msg}), 400
        
    return jsonify({"message": msg}), 200

@admin_bp.route("/users/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    try:
        deleted = delete_user_by_id(user_id)
        if deleted:
            return jsonify({"message": f"User #{user_id} deleted successfully."}), 200
        else:
            return jsonify({"error": f"User #{user_id} not found."}), 404
    except Exception as e:
        return jsonify({"error": f"Failed to delete user: {str(e)}"}), 500               