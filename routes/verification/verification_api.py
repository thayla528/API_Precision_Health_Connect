
from flask import Blueprint, request, jsonify

from services.verification.verification_service import VerificationService


verification_api_bp = Blueprint(
    "verification_api",
    __name__
)


verification_service = VerificationService()


# =====================================================
# INICIAR VERIFICAÇÃO
# =====================================================

@verification_api_bp.route(
    "/api/verification/start",
    methods=["POST"]
)
def start_verification():

    data = request.get_json()

    email = data.get("email")
    phone = data.get("phone")


    if not email:

        return jsonify({

            "success": False,

            "message": "E-mail é obrigatório."

        }), 400


    result = verification_service.create_verification(

        email=email,

        phone=phone

    )


    if not result["success"]:

        return jsonify(result), 400


    return jsonify({

        "success": True,

        "message": "Código de verificação enviado.",

        "verification_id": result["verification_id"],

        "email_sent": result["email_sent"]

    }), 200


# =====================================================
# VERIFICAR E-MAIL
# =====================================================

@verification_api_bp.route(
    "/api/verification/email",
    methods=["POST"]
)
def verify_email():

    data = request.get_json()

    verification_id = data.get("verification_id")
    code = data.get("code")


    if not verification_id or not code:

        return jsonify({

            "success": False,

            "message": "ID da verificação e código são obrigatórios."

        }), 400


    result = verification_service.verify_email(

        verification_id,

        code

    )


    status = 200 if result["success"] else 400


    return jsonify(result), status

