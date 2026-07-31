from flask import Blueprint, request, jsonify

from database.user_model import UserModel
from services.user_service import UserService

from flask_jwt_extended import jwt_required
from security.permissions import role_required

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
@jwt_required()
@role_required("administrator")
def get_active_users():

    users = UserModel.get_active_users()


    return jsonify({

        "success": True,

        "total": len(users),

        "users": [
            {
                "id": user["id"],
                "full_name": user["full_name"],
                "email": user["email"],
                "role": user["role"],
                "profile_type": user["profile_type"],
                "active": user["active"],
                "profile_photo": user["profile_photo"],
                "created_at": user["created_at"]
            }
            for user in users
        ]

    }), 200