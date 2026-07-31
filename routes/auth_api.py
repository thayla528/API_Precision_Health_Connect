from flask import Blueprint, request, jsonify

from services.auth_service import AuthService


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


    return jsonify(result)