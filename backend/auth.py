from flask import Blueprint, request, jsonify
from models import users_collection
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import datetime
import os
from functools import wraps
from dotenv import load_dotenv

load_dotenv()

auth_bp = Blueprint("auth", __name__)

JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")

# Middleware to verify JWT token
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get("Authorization")

        if not token:
            return jsonify({"error": "Token is missing!"}), 401

        try:
            token = token.split(" ")[1]  # Extract actual token from "Bearer <token>"
            data = jwt.decode(token, JWT_SECRET_KEY, algorithms=["HS256"])
            current_user = users_collection.find_one({"email": data["sub"]})  # Using email (sub)

            if not current_user:
                return jsonify({"error": "User not found!"}), 401

        except jwt.ExpiredSignatureError:
            return jsonify({"error": "Token expired!"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"error": "Invalid token!"}), 401

        return f(current_user, *args, **kwargs)

    return decorated

# 🔹 Register User
@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    if not data or "email" not in data or "password" not in data:
        return jsonify({"error": "Email and password required!"}), 400

    if users_collection.find_one({"email": data["email"]}):
        return jsonify({"error": "User already exists!"}), 400

    hashed_password = generate_password_hash(data["password"], method="pbkdf2:sha256")

    user = {
        "email": data["email"],
        "password": hashed_password,
        "created_at": datetime.datetime.utcnow()
    }

    users_collection.insert_one(user)

    return jsonify({"message": "User registered successfully!"}), 201

# 🔹 Login User
@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    if not data or "email" not in data or "password" not in data:
        return jsonify({"error": "Email and password required!"}), 400

    user = users_collection.find_one({"email": data["email"]})

    if not user or not check_password_hash(user["password"], data["password"]):
        return jsonify({"error": "Invalid credentials!"}), 401

    token = jwt.encode(
        {
            "sub": user["email"],  # Added email as subject (sub)
            "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1)
        },
        JWT_SECRET_KEY,
        algorithm="HS256"
    )

    return jsonify({"token": token}), 200

# 🔹 Protected Route Example
@auth_bp.route("/protected", methods=["GET"])
@token_required
def protected_route(current_user):
    return jsonify({"message": "This is a protected route", "user": current_user["email"]}), 200
