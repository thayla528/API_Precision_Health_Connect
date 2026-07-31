from flask import Blueprint, request, jsonify

from services.message_service import MessageService

message_bp = Blueprint("messages", __name__)

@message_bp.route("/messages", methods=["POST"])
def send_message():

    data = request.get_json()

    # Verifica se foi enviado um JSON
    if not data:
        return jsonify({
            "success": False,
            "message": "Nenhum dado enviado."
        }), 400

    sender_id = data.get("sender_id")
    receiver_id = data.get("receiver_id")
    message = data.get("message")

    result = MessageService.send_message(
        sender_id,
        receiver_id,
        message
    )

    if result["success"]:
        return jsonify(result), 201

    return jsonify(result), 400

@message_bp.route("/messages/<int:user_id>", methods=["GET"])
def get_received_messages(user_id):

    result = MessageService.get_received_messages(user_id)

    if result["success"]:
        return jsonify(result), 200

    return jsonify(result), 404

@message_bp.route(
    "/messages/conversation/<int:user1_id>/<int:user2_id>",
    methods=["GET"]
)
def get_conversation(user1_id, user2_id):

    result = MessageService.get_conversation(
        user1_id,
        user2_id
    )

    if result["success"]:
        return jsonify(result), 200

    return jsonify(result), 404

@message_bp.route(
    "/messages/<int:message_id>/read",
    methods=["PUT"]
)
def mark_as_read(message_id):

    result = MessageService.mark_as_read(message_id)

    if result["success"]:
        return jsonify(result), 200

    return jsonify(result), 404

@message_bp.route(
    "/messages/<int:message_id>",
    methods=["DELETE"]
)
def delete_message(message_id):

    result = MessageService.delete_message(message_id)

    if result["success"]:
        return jsonify(result), 200

    return jsonify(result), 404