from flask import Blueprint, request, jsonify

from database.administrators.administrator_entity_model import (
    AdministratorEntityModel
)

from services.users.user_service import UserService

from security.permissions import role_required

from flask_jwt_extended import jwt_required, get_jwt_identity

from utils.file_utils import save_profile_photo

administrator_api_bp = Blueprint(
    "administrator_api",
    __name__
)

user_service = UserService()


@administrator_api_bp.route(
    "/administrators",
    methods=["GET"]
)
@jwt_required()
@role_required("administrator")
def get_administrators():

    search = request.args.get(
        "search",
        default=None,
        type=str
    )

    status = request.args.get(
        "status",
        default=None,
        type=str
    )

    page = request.args.get(
        "page",
        default=1,
        type=int
    )

    per_page = request.args.get(
        "per_page",
        default=10,
        type=int
    )

    if page < 1:
        page = 1

    if per_page < 1:
        per_page = 10

    if per_page > 100:
        per_page = 100

    if search:
        search = search.strip()

        if not search:
            search = None

    if status:
        status = status.lower().strip()

        if status not in ["ativo", "inativo"]:
            return jsonify({
                "success": False,
                "message": "Status inválido."
            }), 400

    result = AdministratorEntityModel.get_all(
        search=search,
        status=status,
        page=page,
        per_page=per_page
    )

    return jsonify({

        "success": True,

        "total": result["total"],

        "pagination": {
            "page": result["page"],
            "per_page": result["per_page"],
            "total": result["total"],
            "total_pages": result["total_pages"]
        },

        "administrators": [

            {
                "id": administrator["id"],
                "user_id": administrator["user_id"],
                "full_name": administrator["full_name"],
                "email": administrator["email"],
                "phone": administrator["phone"],
                "role": administrator["role"],
                "profile_type": administrator["profile_type"],
                "profile_photo": administrator["profile_photo"],
                "active": administrator["active"],
                "created_at": administrator["created_at"],
                "last_login": administrator["last_login"]
            }

            for administrator in result["administrators"]

        ]

    }), 200








@administrator_api_bp.route(
    "/administrators/<int:administrator_id>",
    methods=["PUT"]
)
@jwt_required()
@role_required("administrator")
def update_administrator(administrator_id):

    print("\n========= ARQUIVOS NA REQUISIÇÃO DA API =========")
    print("Files:", request.files)
    print("==================================================\n")

    profile_photo_path = request.form.get("profile_photo")

    print("--- DEBUG UPDATE ADMINISTRATOR ---")
    print("Arquivos recebidos na requisição:", request.files)
    print("Dados de texto recebidos:", request.form)

    if "profile_photo" in request.files:
        file = request.files["profile_photo"]
        print(f"Arquivo detectado: Nome='{file.filename}', Tipo='{file.mimetype}'")

        if file and file.filename != "":
            uploaded_path = save_profile_photo(file)
            print("Resultado do save_profile_photo:", uploaded_path)

            if not uploaded_path:
                print("ERRO: save_profile_photo retornou None! Extensão inválida ou rejeitada.")
                return jsonify({
                    "success": False,
                    "message": "Extensão de arquivo não permitida ou erro no salvamento."
                }), 400
            profile_photo_path = uploaded_path

    full_name = request.form.get("full_name")
    email = request.form.get("email")
    password = request.form.get("password")
    phone = request.form.get("phone")

    password_param = password if password and password.strip() != "" else None

    result = user_service.update_administrator(
        administrator_id=administrator_id,
        full_name=full_name,
        email=email,
        password=password_param,

        profile_photo=profile_photo_path,

        phone=phone
    )

    print("Resultado do UserService:", result)
    print("----------------------------------")

    if not result["success"]:
        return jsonify(result), 400

    return jsonify({
        "success": True,
        "message": "Administrador atualizado com sucesso.",
        "administrator": {
            "id": administrator_id,
            "full_name": full_name,
            "email": email,
            "phone": phone,
            "profile_photo": profile_photo_path
        }
    }), 200


@administrator_api_bp.route(
    "/administrators",
    methods=["POST"]
)
@jwt_required()
@role_required("administrator")
def create_administrator():

    data = request.get_json(silent=True)

    if not data:
        return jsonify({
            "success": False,
            "message": "Dados não enviados."
        }), 400

    full_name = data.get("full_name")
    email = data.get("email")
    password = data.get("password")
    profile_photo = data.get("profile_photo")
    phone = data.get("phone")

    result = user_service.create_administrator(
        full_name=full_name,
        email=email,
        password=password,
        profile_photo=profile_photo,
        phone=phone
    )

    if not result["success"]:
        return jsonify(result), 400

    return jsonify(result), 201


@administrator_api_bp.route(
    "/administrators/<int:administrator_id>",
    methods=["PUT"]
)



@administrator_api_bp.route(
    "/administrators/<int:administrator_id>/deactivate",
    methods=["PUT"]
)
@jwt_required()
@role_required("administrator")
def deactivate_administrator(administrator_id):
    admin_id = get_jwt_identity()

    result = user_service.deactivate_administrator(
        admin_id,
        administrator_id
    )

    if not result["success"]:
        return jsonify(result), 400

    return jsonify(result), 200


@administrator_api_bp.route(
    "/administrators/<int:administrator_id>/activate",
    methods=["PUT"]
)
@jwt_required()
@role_required("administrator")
def activate_administrator(administrator_id):
    admin_id = get_jwt_identity()

    result = user_service.activate_administrator(
        admin_id,
        administrator_id
    )

    if not result["success"]:
        return jsonify(result), 400

    return jsonify(result), 200
