from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import tasks_collection
from bson import ObjectId

tasks_bp = Blueprint("tasks", __name__)

# ✅ Create Task (POST)
@tasks_bp.route("/create", methods=["POST"])
def create_task():
    try:
        data = request.get_json()
        if not data or "title" not in data or "description" not in data:
            return jsonify({"error": "Title and description are required"}), 400

        task = {
            "title": data.get("title"),
            "description": data.get("description"),
            "assigned_to": data.get("assigned_to", None),
            "status": "pending"
        }

        result = tasks_collection.insert_one(task)
        return jsonify({"msg": "Task created successfully", "task_id": str(result.inserted_id)}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ✅ Get All Tasks (GET)
@tasks_bp.route("/", methods=["GET"])
@jwt_required()
def get_tasks():
    tasks = list(tasks_collection.find({}, {"_id": 1, "title": 1, "description": 1, "status": 1, "assigned_to": 1, "created_by": 1}))
    for task in tasks:
        task["_id"] = str(task["_id"])
    return jsonify(tasks), 200

# ✅ Get Single Task by ID (GET)
@tasks_bp.route("/<task_id>", methods=["GET"])
@jwt_required()
def get_task(task_id):
    task = tasks_collection.find_one({"_id": ObjectId(task_id)})
    if not task:
        return jsonify({"msg": "Task not found"}), 404
    task["_id"] = str(task["_id"])
    return jsonify(task), 200

# ✅ Update Task (PUT)
@tasks_bp.route("/update/<task_id>", methods=["PUT"])
@jwt_required()
def update_task(task_id):
    data = request.get_json()
    update_fields = {key: data[key] for key in ["title", "description", "assigned_to", "status"] if key in data}
    
    result = tasks_collection.update_one({"_id": ObjectId(task_id)}, {"$set": update_fields})
    
    if result.modified_count == 0:
        return jsonify({"msg": "Task not updated or doesn't exist"}), 400

    return jsonify({"msg": "Task updated successfully"}), 200

# ✅ Delete Task (DELETE)
@tasks_bp.route("/delete/<task_id>", methods=["DELETE"])
@jwt_required()
def delete_task(task_id):
    result = tasks_collection.delete_one({"_id": ObjectId(task_id)})

    if result.deleted_count == 0:
        return jsonify({"msg": "Task not found"}), 404

    return jsonify({"msg": "Task deleted successfully"}), 200
