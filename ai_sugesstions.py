from flask import Blueprint, request, jsonify
import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

gemini_api_key = os.getenv("GEMINI_API_KEY")
if not gemini_api_key:
    raise ValueError("GEMINI_API_KEY is not set in environment variables")

genai.configure(api_key=gemini_api_key)

ai_bp = Blueprint("ai_suggestions", __name__)

@ai_bp.route("/suggest", methods=["POST"])
def ai_suggest():
    data = request.get_json()
    query = data.get("query")

    if not query:
        return jsonify({"error": "Query is required"}), 400
    
    try:
        model = genai.GenerativeModel("gemini-pro")
        response = model.generate_content(query)
        suggestion = response.text if hasattr(response, "text") else "No response received."
        return jsonify({"suggestion": suggestion}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
