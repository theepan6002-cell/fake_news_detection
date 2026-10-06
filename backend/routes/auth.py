import re
from flask import Blueprint, request, jsonify
from backend.database.db import (
    create_user,
    authenticate_user,
    get_user_by_id,
    update_user_profile,
    update_user_password,
    create_password_reset_token,
    reset_password_with_token,
    get_user_prediction_stats
)

auth_bp = Blueprint("auth", __name__)

EMAIL_REGEX = r"^[\w\.-]+@[\w\.-]+\.\w+$"

@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json() or {}
    full_name = data.get("full_name", "").strip()
    username = data.get("username", "").strip()
    email = data.get("email", "").strip().lower()
    password = data.get("password", "")
    confirm_password = data.get("confirm_password", "")
    
    # Validation
    if not full_name or not username or not email or not password:
        return jsonify({"error": "All required fields must be filled."}), 400
        
    if not re.match(EMAIL_REGEX, email):
        return jsonify({"error": "Please enter a valid email address."}), 400
        
    if len(password) < 6:
        return jsonify({"error": "Password must be at least 6 characters long."}), 400
        
    if password != confirm_password:
        return jsonify({"error": "Password and Confirm Password do not match."}), 400
        
    user, err = create_user(full_name, username, email, password, role="user")
    if err:
        return jsonify({"error": err}), 400
        
    return jsonify({
        "message": "Account created successfully! You may now log in.",
        "user": user
    }), 201

@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json() or {}
    identifier = data.get("email", data.get("identifier", "")).strip()
    password = data.get("password", "")
    
    if not identifier or not password:
        return jsonify({"error": "Email/Username and password are required."}), 400
        
    user, err = authenticate_user(identifier, password)
    if err:
        return jsonify({"error": err}), 401
        
    stats = get_user_prediction_stats(user["id"])
    user["stats"] = stats
    
    return jsonify({
        "message": f"Welcome back, {user['full_name']}!",
        "user": user
    }), 200

@auth_bp.route("/me", methods=["GET"])
def get_current_user():
    user_id = request.args.get("user_id")
    if not user_id:
        return jsonify({"error": "User ID parameter is required."}), 400
        
    user = get_user_by_id(user_id)
    if not user:
        return jsonify({"error": "User not found."}), 404
        
    stats = get_user_prediction_stats(user["id"])
    user["stats"] = stats
    return jsonify({"user": user}), 200

@auth_bp.route("/profile", methods=["PUT"])
def update_profile():
    data = request.get_json() or {}
    user_id = data.get("user_id")
    full_name = data.get("full_name", "").strip()
    email = data.get("email", "").strip().lower()
    
    if not user_id or not full_name or not email:
        return jsonify({"error": "User ID, full name, and email are required."}), 400
        
    if not re.match(EMAIL_REGEX, email):
        return jsonify({"error": "Please enter a valid email address."}), 400
        
    updated_user, err = update_user_profile(user_id, full_name, email)
    if err:
        return jsonify({"error": err}), 400
        
    stats = get_user_prediction_stats(updated_user["id"])
    updated_user["stats"] = stats
    
    return jsonify({
        "message": "Profile updated successfully.",
        "user": updated_user
    }), 200

@auth_bp.route("/change-password", methods=["PUT"])
def change_password():
    data = request.get_json() or {}
    user_id = data.get("user_id")
    old_password = data.get("old_password", "")
    new_password = data.get("new_password", "")
    
    if not user_id or not old_password or not new_password:
        return jsonify({"error": "Current password and new password are required."}), 400
        
    if len(new_password) < 6:
        return jsonify({"error": "New password must be at least 6 characters long."}), 400
        
    success, msg = update_user_password(user_id, old_password, new_password)
    if not success:
        return jsonify({"error": msg}), 400
        
    return jsonify({"message": msg}), 200

@auth_bp.route("/forgot-password", methods=["POST"])
def forgot_password():
    data = request.get_json() or {}
    email = data.get("email", "").strip().lower()
    
    if not email:
        return jsonify({"error": "Please enter your registered email address."}), 400
        
    res, err = create_password_reset_token(email)
    if err:
        return jsonify({"error": err}), 404
        
    return jsonify({
        "message": f"Password reset token issued for {res['name']}.",
        "reset_token": res["token"],
        "email": res["email"]
    }), 200

@auth_bp.route("/reset-password", methods=["POST"])
def reset_password():
    data = request.get_json() or {}
    token = data.get("token", "").strip()
    new_password = data.get("new_password", "")
    
    if not token or not new_password:
        return jsonify({"error": "Reset token and new password are required."}), 400
        
    if len(new_password) < 6:
        return jsonify({"error": "New password must be at least 6 characters long."}), 400
        
    success, msg = reset_password_with_token(token, new_password)
    if not success:
        return jsonify({"error": msg}), 400
        
    return jsonify({"message": msg}), 200
