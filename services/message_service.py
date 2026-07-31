from database.message_model import MessageModel
from database.user_model import UserModel


class MessageService:

    @staticmethod
    def send_message(sender_id, receiver_id, message):

        sender = UserModel.get_by_id(sender_id)

        if sender is None:
            return {
                "success": False,
                "message": "Remetente não encontrado."
            }

        receiver = UserModel.get_by_id(receiver_id)

        if receiver is None:
            return {
                "success": False,
                "message": "Destinatário não encontrado."
            }

        if not message.strip():
            return {
                "success": False,
                "message": "Digite uma mensagem."
            }

        message_id = MessageModel.send_message(
            sender_id,
            receiver_id,
            message
        )

        return {
            "success": True,
            "message": "Mensagem enviada com sucesso.",
            "message_id": message_id
        }

    @staticmethod
    def get_received_messages(user_id):

        user = UserModel.get_by_id(user_id)

        if user is None:
            return {
                "success": False,
                "message": "Usuário não encontrado."
            }

        messages = MessageModel.get_received_messages(user_id)

        return {
            "success": True,
            "messages": messages
        }

    @staticmethod
    def get_conversation(user1_id, user2_id):

        user1 = UserModel.get_by_id(user1_id)

        if user1 is None:
            return {
                "success": False,
                "message": "Primeiro usuário não encontrado."
            }

        user2 = UserModel.get_by_id(user2_id)

        if user2 is None:
            return {
                "success": False,
                "message": "Segundo usuário não encontrado."
            }

        conversation = MessageModel.get_conversation(
            user1_id,
            user2_id
        )

        return {
            "success": True,
            "conversation": conversation
        }

    @staticmethod
    def mark_as_read(message_id):

        rows_updated = MessageModel.mark_as_read(message_id)

        if rows_updated == 0:
            return {
                "success": False,
                "message": "Mensagem não encontrada."
            }

        return {
            "success": True,
            "message": "Mensagem marcada como lida."
        }

    @staticmethod
    def delete_message(message_id):

        rows_deleted = MessageModel.delete_message(message_id)

        if rows_deleted == 0:
            return {
                "success": False,
                "message": "Mensagem não encontrada."
            }

        return {
            "success": True,
            "message": "Mensagem removida com sucesso."
        }