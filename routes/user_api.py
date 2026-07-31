from flask import Blueprint, request, jsonify

from database.user_model import UserModel
from services.user_service import UserService


user_api_bp = Blueprint(
    "user_api_bp",
    __name__
)


user_service = UserService()


@user_api_bp.route("/api/register", methods=["POST"])
def register():

    data = request.json

    result = user_service.register_user(
        data["invitation_code"],
        data["password"],
        data.get("profile_photo")
    )

    return jsonify(result)



@user_api_bp.route(
    "/users/active",
    methods=["GET"]
)
@user_api_bp.route("/users/active", methods=["GET"])
def get_active_users():

    users = UserModel.get_active_users()


    return jsonify({

        "success": True,

        "total": len(users),

        "users": [
            dict(user)
            for user in users
        ]

    }), 200