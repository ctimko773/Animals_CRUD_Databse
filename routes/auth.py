from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from database import get_db
from auth import hash_password, verify_password

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")


@auth_bp.post("/register")
def register():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"error": "Username and password required"}), 400

    db = get_db()
    if db.users.find_one({"username": username}):
        return jsonify({"error": "Username already taken"}), 400

    db.users.insert_one({
        "username": username,
        "password": hash_password(password)
    })
    return jsonify({"message": "User created"}), 201


@auth_bp.post("/login")
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"error": "Username and password required"}), 400

    db = get_db()
    user = db.users.find_one({"username": username})

    if not user or not verify_password(password, user["password"]):
        return jsonify({"error": "Invalid credentials"}), 401

    access_token = create_access_token(identity=username)
    return jsonify({"access_token": access_token, "token_type": "bearer"}), 200