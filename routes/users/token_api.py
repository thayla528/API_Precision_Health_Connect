from flask import Blueprint, jsonify

from flask_jwt_extended import (
    jwt_required,
    get_jwt_identity,
    create_access_token
)



token_bp = Blueprint(
    "token_api",
    __name__
)





# =====================================================
# REFRESH TOKEN
# =====================================================

@token_bp.route(
    "/refresh",
    methods=["POST"]
)
@jwt_required(
    refresh=True
)
def refresh_token():


    user_id = get_jwt_identity()



    new_access_token = create_access_token(

        identity=str(user_id)

    )



    return jsonify({

        "success": True,

        "access_token": new_access_token

    }), 200