from flask import Blueprint, request, jsonify

from database.user_model import UserModel
from services.invitation_service import InvitationService


invitation_api_bp = Blueprint(
    "invitation_api",
    __name__
)


invitation_service = InvitationService()


# =====================================================
# LISTAR TODAS AS SOLICITAÇÕES
# =====================================================

@invitation_api_bp.route(
    "/api/invitations",
    methods=["GET"]
)
def get_all_invitations():

    invitations = invitation_service.get_all_invitations()


    return jsonify({

        "success": True,

        "invitations": invitations,

        "total": len(invitations)

    }), 200


# =====================================================
# FINALIZAR CADASTRO PELO CONVITE
# =====================================================

@invitation_api_bp.route(
    "/register",
    methods=["POST"]
)
def register_with_invitation():

    data = request.get_json()


    invitation_code = data.get("invitation_code")

    password = data.get("password")



    if not invitation_code or not password:

        return jsonify({

            "success": False,

            "message": "Código e senha são obrigatórios."

        }), 400



    result = invitation_service.register_with_invitation(

        invitation_code,

        password

    )


    status = 200 if result["success"] else 400


    return jsonify(result), status

# =====================================================
# VER DETALHES DE UMA SOLICITAÇÃO
# =====================================================

@invitation_api_bp.route(
    "/invitations/<int:id>",
    methods=["GET"]
)
def get_invitation(id):

    invitation = invitation_service.invitation_model.get_by_id(id)

    if not invitation:

        return jsonify({
            "success": False,
            "message": "Invitation not found"
        }), 404


    return jsonify(dict(invitation)), 200



# =====================================================
# APROVAR SOLICITAÇÃO
# =====================================================

@invitation_api_bp.route(
    "/admin/invitations/<int:id>/approve",
    methods=["POST"]
)
def approve_invitation(id):

    administrator_id = 1


    result = invitation_service.approve_invitation(
        id,
        administrator_id
    )


    status = 200 if result["success"] else 400


    return jsonify(result), status



# =====================================================
# REJEITAR SOLICITAÇÃO
# =====================================================

@invitation_api_bp.route(
    "/admin/invitations/<int:id>/reject",
    methods=["POST"]
)
def reject_invitation(id):

    administrator_id = 1


    result = invitation_service.reject_invitation(
        id,
        administrator_id
    )


    status = 200 if result["success"] else 400


    return jsonify(result), status



# =====================================================
# CRIAR SOLICITAÇÃO DE CONVITE
# =====================================================

@invitation_api_bp.route(
    "/api/invitation",
    methods=["POST"]
)
def request_invitation():

    data = request.get_json()


    result = invitation_service.request_invitation(

        full_name=data.get("full_name"),

        email=data.get("email"),

        phone=data.get("phone"),

        birth_date=data.get("birth_date"),

        profile_type=data.get("profile_type"),

        interest_reason=data.get("interest")

    )


    if result["success"]:

        return jsonify(result), 201


    return jsonify(result), 400

# =====================================================
# FINALIZAR CADASTRO PELO CONVITE
# =====================================================

@invitation_api_bp.route(
    "/api/register",
    methods=["POST"]
)
def register_user():

    data = request.get_json()


    invitation_code = data.get("invitation_code")
    password = data.get("password")


    if not invitation_code or not password:

        return jsonify({

            "success": False,
            "message": "Código e senha são obrigatórios."

        }), 400



    invitation = invitation_service.invitation_model.get_by_code(
        invitation_code
    )


    if not invitation:

        return jsonify({

            "success": False,
            "message": "Convite não encontrado."

        }), 404



    invitation = dict(invitation)



    if invitation["status"] != "approved":

        return jsonify({

            "success": False,
            "message": "Convite ainda não aprovado."

        }), 400



    if invitation["used"] == 1:

        return jsonify({

            "success": False,
            "message": "Convite já utilizado."

        }), 400



    # criar usuário

    user_id = +UserModel.create(

        invitation_id=invitation["id"],

        full_name=invitation["full_name"],

        email=invitation["email"],

        password=password,

        profile_type=invitation["profile_type"],

        profile_photo=None

    )


    # marcar convite como usado

    invitation_service.invitation_model.mark_as_used(
        invitation["id"]
    )


    return jsonify({

        "success": True,

        "message": "Cadastro concluído.",

        "user_id": user_id

    }), 201