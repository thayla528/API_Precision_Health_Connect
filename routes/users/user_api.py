from flask import Blueprint, request, jsonify

from database.users.user_model import UserModel
from services.users.user_service import UserService


from security.permissions import role_required

from services.audit.audit_service import AuditService

from flask_jwt_extended import (
    jwt_required,
    get_jwt_identity
)

user_api_bp = Blueprint(
    "user_api_bp",
    __name__
)


user_service = UserService()

audit_service = AuditService()



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

@user_api_bp.route(
    "/users/<int:user_id>/deactivate",
    methods=["PUT"]
)
@jwt_required()
@role_required("administrator")
def deactivate_user(user_id):


    admin_id = get_jwt_identity()


    result = user_service.deactivate_user(

        admin_id,

        user_id

    )


    if not result["success"]:

        return jsonify(result), 400


    return jsonify(result), 200