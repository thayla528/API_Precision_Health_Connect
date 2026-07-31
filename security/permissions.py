from functools import wraps

from flask import jsonify

from flask_jwt_extended import get_jwt_identity

from database.user_model import UserModel


def role_required(required_role):

    def decorator(function):

        @wraps(function)
        def wrapper(*args, **kwargs):

            user_id = get_jwt_identity()

            user = UserModel.get_by_id(
                user_id
            )


            if user is None:
                return jsonify({
                    "success": False,
                    "message": "Usuário não encontrado."
                }), 404


            if user["role"] != required_role:

                return jsonify({
                    "success": False,
                    "message": "Permissão negada."
                }), 403


            return function(
                *args,
                **kwargs
            )


        return wrapper

    return decorator