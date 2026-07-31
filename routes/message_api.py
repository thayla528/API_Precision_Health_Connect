from flask import Blueprint, request, jsonify



from services.message_service import MessageService

from flask_jwt_extended import jwt_required, get_jwt_identity


message_bp = Blueprint("messages", __name__)

@message_bp.route("/messages", methods=["POST"])
@jwt_required()
def send_message():

    data = request.get_json()

    # Verifica se foi enviado um JSON
    if not data:
        return jsonify({
            "success": False,
            "message": "Nenhum dado enviado."
        }), 400

    sender_id = get_jwt_identity()

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
@jwt_required()
def get_received_messages(user_id):

    current_user_id = get_jwt_identity()

    if int(current_user_id) != user_id:
        return jsonify({
            "success": False,
            "message": "Acesso não autorizado."
        }), 403


    result = MessageService.get_received_messages(user_id)


    if result["success"]:
        return jsonify(result), 200


    return jsonify(result), 404

@message_bp.route(
    "/messages/conversation/<int:user1_id>/<int:user2_id>",
    methods=["GET"]
)
@jwt_required()
def get_conversation(user1_id, user2_id):

    current_user_id = int(get_jwt_identity())


    if current_user_id not in [
        user1_id,
        user2_id
    ]:
        return jsonify({
            "success": False,
            "message": "Acesso não autorizado."
        }), 403


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