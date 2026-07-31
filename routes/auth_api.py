from flask import Blueprint, request, jsonify

from services.auth_service import AuthService

from flask_jwt_extended import create_access_token

auth_api_bp = Blueprint(
    "auth_api",
    __name__
)


auth_service = AuthService()


@auth_api_bp.route("/login", methods=["POST"])
def login():

    data = request.json


    if not data:
        return jsonify({
            "success": False,
            "message": "No data provided."
        }), 400


    email = data.get("email")
    password = data.get("password")


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
        access_token = create_access_token(
            identity=str(result["user"]["id"])
        )

        result["access_token"] = access_token

    return jsonify(result)