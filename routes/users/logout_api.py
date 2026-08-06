from flask import Blueprint, jsonify

from flask_jwt_extended import (
    jwt_required,
    get_jwt
)

from database.security.revoked_token_model import RevokedTokenModel



logout_bp = Blueprint(
    "logout_api",
    __name__
)



@logout_bp.route(
    "/logout",
    methods=["POST"]
)
@jwt_required()
def logout():


    token = get_jwt()


    jti = token["jti"]


    RevokedTokenModel.add_token(
        jti
    )


    return jsonify({

        "success": True,

        "message": "Logout successful."

    }), 200