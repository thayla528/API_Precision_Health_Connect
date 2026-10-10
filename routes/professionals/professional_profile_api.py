
from flask import Blueprint, request, jsonify

from flask_jwt_extended import (
    jwt_required,
    get_jwt_identity
)

from services.professionals.professional_profile_service import (
    ProfessionalProfileService
)

from security.permissions import role_required

from utils.file_utils import save_profile_photo


professional_profile_bp = Blueprint(
    "professional_profile",
    __name__,
    url_prefix="/professional"
)


service = ProfessionalProfileService()


# =====================================================
# CREATE PROFESSIONAL PROFILE
# =====================================================

@professional_profile_bp.route(
    "/profile",
    methods=["POST"]
)
@jwt_required()

def create_profile():

    user_id = get_jwt_identity()

    data = request.get_json(
        silent=True
    )


    # =================================================
    # VALIDAR JSON
    # =================================================

    if not data:

        return jsonify({

            "success": False,

            "message":
                "JSON body is required"

        }), 400


    # =================================================
    # DADOS OBRIGATÓRIOS
    # =================================================

    specialty = data.get(
        "specialty"
    )

    license_number = data.get(
        "license_number"
    )


    if not specialty or not license_number:

        return jsonify({

            "success": False,

            "message":
                "specialty and license_number are required"

        }), 400


    # =================================================
    # CRIAR PERFIL
    # =================================================

    result = service.create_profile(

        user_id,

        specialty,

        license_number,

        data.get("institution"),

        data.get("practice_area"),

        data.get("phone"),

        data.get("professional_email")

    )


    # =================================================
    # ERRO
    # =================================================

    if not result["success"]:

        return jsonify(result), 400


    # =================================================
    # SUCESSO
    # =================================================

    return jsonify(result), 201


# =====================================================
# GET PROFESSIONAL PROFILE
# =====================================================

@professional_profile_bp.route(
    "/profile",
    methods=["GET"]
)
@jwt_required()
@role_required("professional")
def get_profile():

    user_id = get_jwt_identity()


    # =================================================
    # BUSCAR PERFIL
    # =================================================

    result = service.get_profile(
        user_id
    )


    # =================================================
    # ERRO
    # =================================================

    if not result["success"]:

        return jsonify(result), 404


    professional = result["professional"]


    # =================================================
    # RESPOSTA
    # =================================================

    return jsonify({

        "success": True,

        "professional": {

            # ---------------- USERS ----------------

            "id": professional["id"],

            "user_id": professional["user_id"],

            "full_name": professional["full_name"],

            "email": professional["email"],

            "role": professional["role"],

            "profile_type": professional["profile_type"],

            "profile_photo": professional["profile_photo"],

            "active": professional["active"],

            "last_login": professional["last_login"],

            "created_at": professional["created_at"],


            # ---------------- PROFESSIONALS ----------------

            "specialty": professional["specialty"],

            "license_number": professional["license_number"],

            "institution": professional["institution"],

            "practice_area": professional["practice_area"],

            "phone": professional["phone"],

            "professional_email":
                professional["professional_email"]

        }

    }), 200


# =====================================================
# UPDATE PROFESSIONAL PROFILE
# =====================================================

@professional_profile_bp.route(
    "/profile",
    methods=["PUT"]
)
@jwt_required()
@role_required("professional")
def update_profile():

    user_id = get_jwt_identity()


    # =================================================
    # DEBUG
    # =================================================

    print(
        "\n========= ARQUIVOS NA REQUISIÇÃO "
        "DO PROFESSIONAL ========="
    )

    print(
        "Files:",
        request.files
    )

    print(
        "==================================================\n"
    )


    print(
        "--- DEBUG UPDATE PROFESSIONAL PROFILE ---"
    )

    print(
        "Arquivos recebidos:",
        request.files
    )

    print(
        "Dados de texto recebidos:",
        request.form
    )


    # =================================================
    # FOTO DE PERFIL
    # =================================================

    profile_photo_path = request.form.get(
        "profile_photo"
    )


    if "profile_photo" in request.files:

        file = request.files[
            "profile_photo"
        ]


        print(
            f"Arquivo detectado: "
            f"Nome='{file.filename}', "
            f"Tipo='{file.mimetype}'"
        )


        if file and file.filename != "":

            uploaded_path = save_profile_photo(
                file
            )


            print(
                "Resultado do save_profile_photo:",
                uploaded_path
            )


            if not uploaded_path:

                print(
                    "ERRO: save_profile_photo "
                    "retornou None!"
                )

                return jsonify({

                    "success": False,

                    "message":
                        "Extensão de arquivo não permitida "
                        "ou erro no salvamento."

                }), 400


            profile_photo_path = uploaded_path


    # =================================================
    # DADOS DA TABELA USERS
    # =================================================

    full_name = request.form.get(
        "full_name"
    )

    email = request.form.get(
        "email"
    )

    password = request.form.get(
        "password"
    )


    # =================================================
    # DADOS DA TABELA PROFESSIONALS
    # =================================================

    specialty = request.form.get(
        "specialty"
    )

    license_number = request.form.get(
        "license_number"
    )

    institution = request.form.get(
        "institution"
    )

    practice_area = request.form.get(
        "practice_area"
    )

    phone = request.form.get(
        "phone"
    )

    professional_email = request.form.get(
        "professional_email"
    )


    # =================================================
    # SENHA
    # =================================================

    password_param = (

        password
        if password
        and password.strip() != ""
        else None

    )


    # =================================================
    # ATUALIZAR PERFIL
    # =================================================

    result = service.update_profile(

        user_id=user_id,

        full_name=full_name,

        email=email,

        password=password_param,

        profile_photo=profile_photo_path,

        specialty=specialty,

        license_number=license_number,

        institution=institution,

        practice_area=practice_area,

        phone=phone,

        professional_email=professional_email

    )


    # =================================================
    # DEBUG RESULTADO
    # =================================================

    print(
        "Resultado do ProfessionalProfileService:",
        result
    )

    print(
        "----------------------------------"
    )


    # =================================================
    # ERRO
    # =================================================

    if not result["success"]:

        return jsonify(result), 400


    # =================================================
    # SUCESSO
    # =================================================

    professional = result.get(
        "professional"
    )


    return jsonify({

        "success": True,

        "message":
            "Perfil profissional atualizado com sucesso.",

        "professional": {

            "id":
                professional["professional_id"],

            "user_id":
                user_id,

            "full_name":
                professional["full_name"],

            "email":
                professional["email"],

            "profile_photo":
                professional["profile_photo"],

            "specialty":
                professional["specialty"],

            "license_number":
                professional["license_number"],

            "institution":
                professional["institution"],

            "practice_area":
                professional["practice_area"],

            "phone":
                professional["phone"],

            "professional_email":
                professional["professional_email"]

        }

    }), 200

