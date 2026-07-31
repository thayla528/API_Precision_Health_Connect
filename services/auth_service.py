from database.user_model import UserModel

from werkzeug.security import check_password_hash


class AuthService:

    def __init__(self):
        self.user_model = UserModel()


    def login(
        self,
        email,
        password
    ):

        user = self.user_model.get_by_email(email)


        if not user:
            return {
                "success": False,
                "message": "Invalid email or password."
            }


        if user["active"] == 0:
            return {
                "success": False,
                "message": "User account is inactive."
            }


        if not check_password_hash(
            user["password"],
            password
        ):
            return {
                "success": False,
                "message": "Invalid email or password."
            }


        self.user_model.update_last_login(
            user["id"]
        )

        return {
            "success": True,
            "message": "Login successful.",
            "user": {
                "id": user["id"],
                "full_name": user["full_name"],
                "email": user["email"],
                "role": user["role"],
                "profile_type": user["profile_type"],
                "active": user["active"],
                "profile_photo": user["profile_photo"]
            }
        }

