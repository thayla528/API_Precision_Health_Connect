
from flask import Blueprint, request, jsonify

from services.users.password_reset_service import PasswordResetService


password_reset_api_bp = Blueprint(
    "password_reset_api",
    __name__
)


password_reset_service = PasswordResetService()


# =====================================================
# SOLICITAR RECUPERAÇÃO DE SENHA
# =====================================================

@password_reset_api_bp.route(
    "/api/password/forgot",
    methods=["POST"]
)
def forgot_password():

    data = request.get_json(
        silent=True
    )


    # =================================================
    # VERIFICAR DADOS
    # =================================================

    if not data:

        return jsonify({

            "success": False,

            "message":
                "Dados não enviados."

        }), 400


    email = data.get("email")


    if not email:

        return jsonify({

            "success": False,

            "message":
                "E-mail é obrigatório."

        }), 400


    # =================================================
    # SOLICITAR RECUPERAÇÃO
    # =================================================

    result = (
        password_reset_service
        .request_password_reset(
            email
        )
    )


    # =================================================
    # RESPOSTA
    # =================================================

    if not result["success"]:

        return jsonify(result), 400


    return jsonify(result), 200




# =====================================================
# VALIDAR LINK DE RECUPERAÇÃO
# =====================================================

@password_reset_api_bp.route(
    "/reset-password/<reset_code>",
    methods=["GET"]
)
def validate_password_reset(
    reset_code
):

    print("")
    print("==============================================")
    print("LINK DE RECUPERAÇÃO ACESSADO")
    print("==============================================")

    print(
        "Reset code recebido:",
        reset_code
    )


    # =================================================
    # VALIDAR TOKEN
    # =================================================

    result = (
        password_reset_service
        .validate_reset_token(
            reset_code
        )
    )


    # =================================================
    # TOKEN INVÁLIDO
    # =================================================

    if not result["success"]:

        print(
            "Token inválido ou expirado."
        )

        print("==============================================")
        print("")

        return jsonify(result), 400


    # =================================================
    # TOKEN VÁLIDO
    # =================================================

    print(
        "Token válido."
    )

    print(
        "Redirecionamento para redefinição de senha."
    )

    print("==============================================")
    print("")


    return jsonify({

        "success": True,

        "message":
            "Link de recuperação válido.",

        "reset_code":
            reset_code

    }), 200

