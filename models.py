from flask import Flask
from flask_pymongo import PyMongo
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# MongoDB Connection
app.config["MONGO_URI"] = os.getenv("MONGO_URI")
mongo = PyMongo(app)
db = mongo.db  # Database Reference

# Collections
users_collection = db.users
tasks_collection = db.tasks
suggestions_collection = db.ai_sugesstions
