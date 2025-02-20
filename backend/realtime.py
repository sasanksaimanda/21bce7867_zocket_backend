from flask import request
from flask_socketio import SocketIO, emit, join_room, leave_room
from flask_jwt_extended import jwt_required, get_jwt_identity

# Initialize SocketIO
socketio = SocketIO(cors_allowed_origins="*")

# Room-based communication
@socketio.on("join")
@jwt_required()
def handle_join(data):
    user_email = get_jwt_identity()
    room = data.get("room", user_email)
    join_room(room)
    emit("message", {"msg": f"{user_email} has joined {room}"}, room=room)

@socketio.on("leave")
@jwt_required()
def handle_leave(data):
    user_email = get_jwt_identity()
    room = data.get("room", user_email)
    leave_room(room)
    emit("message", {"msg": f"{user_email} has left {room}"}, room=room)

@socketio.on("task_update")
@jwt_required()
def handle_task_update(data):
    task_id = data.get("task_id")
    updated_status = data.get("status")
    emit("task_updated", {"task_id": task_id, "status": updated_status}, broadcast=True)
