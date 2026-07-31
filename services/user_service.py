from database.user_model import UserModel
from database.invitation_model import InvitationModel

from werkzeug.security import generate_password_hash


class UserService:

    def __init__(self):
        self.user_model = UserModel()
        self.invitation_model = InvitationModel()


    def register_user(
            self,
            invitation_code,
            password,
            profile_photo
    ):

        if not password:
            return {
                "success": False,
                "message": "Password is required."
            }


        # Buscar convite
        invitation = self.invitation_model.get_by_code(
            invitation_code
        )


        if not invitation:
            return {
                "success": False,
                "message": "Invalid invitation code."
            }


        # Verificar se convite já foi usado
        if invitation["used"] == 1:
            return {
                "success": False,
                "message": "Invitation already used."
            }


        # Verificar aprovação
        if invitation["status"] != "approved":
            return {
                "success": False,
                "message": "Invitation is not approved."
            }


        existing_user = self.user_model.get_by_email(
            invitation["email"]
        )


        if existing_user:
            return {
                "success": False,
                "message": "User already exists."
            }


        hashed_password = generate_password_hash(
            password
        )


        user_id = self.user_model.create(
            invitation["id"],
            invitation["full_name"],
            invitation["email"],
            hashed_password,
            invitation["profile_type"],
            profile_photo
        )


        # Bloquear reutilização do convite
        self.invitation_model.mark_as_used(
            invitation["id"]
        )


        return {
            "success": True,
            "message": "User created successfully.",
            "user_id": user_id
        }