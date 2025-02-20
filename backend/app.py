from flask import Flask, jsonify
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from models import mongo
from auth import auth_bp
from tasks import tasks_bp
from ai_sugesstions import ai_bp
from realtime import socketio

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Configure app with environment variables
app.config["MONGO_URI"] = os.getenv("MONGO_URI")
app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")

# Initialize extensions
mongo.init_app(app)
jwt = JWTManager(app)
CORS(app)
socketio.init_app(app, cors_allowed_origins="*")

# Register Blueprints (API Modules)
app.register_blueprint(auth_bp, url_prefix="/auth")
app.register_blueprint(tasks_bp, url_prefix="/tasks")
app.register_blueprint(ai_bp, url_prefix="/ai")

# Test Route
@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "Task Management System API is running!"}), 200

# Run Flask App with WebSocket Support
if __name__ == "__main__":
    socketio.run(app, debug=True, host="0.0.0.0", port=5000)
