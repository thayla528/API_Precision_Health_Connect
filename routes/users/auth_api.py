from flask import Blueprint, request, jsonify

from services.users.auth_service import AuthService

from security.rate_limit import limiter

from flask_jwt_extended import (
    create_access_token,
    create_refresh_token
)



auth_api_bp = Blueprint(
    "auth_api",
    __name__
)



auth_service = AuthService()





@auth_api_bp.route(
    "/login",
    methods=["POST"]
)
@limiter.limit("5 per minute")
def login():


    data = request.json


    if not data:

        return jsonify({

            "success": False,

            "message": "No data provided."

        }), 400





    email = data.get(
        "email"
    )


    password = data.get(
        "password"
    )





    if not email or not password:

        return jsonify({

            "success": False,

            "message": "Email and password are required."

        }), 400





    result = auth_service.login(

        email,

        password

    )





    if result["success"]:


        user_id = str(
            result["user"]["id"]
        )


        access_token = create_access_token(

            identity=user_id

        )


        refresh_token = create_refresh_token(

            identity=user_id

        )



        result["access_token"] = access_token


        result["refresh_token"] = refresh_token





    return jsonify(result)