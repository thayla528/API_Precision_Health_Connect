from flask import Blueprint, request, jsonify

from flask_jwt_extended import jwt_required, get_jwt_identity

from services.professionals.professional_profile_service import ProfessionalProfileService

from security.permissions import role_required


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
@role_required("professional")
def create_profile():

    user_id = get_jwt_identity()

    data = request.get_json()


    if not data:
        return jsonify({
            "message": "JSON body is required"
        }), 400



    specialty = data.get("specialty")
    license_number = data.get("license_number")


    if not specialty or not license_number:

        return jsonify({
            "message": "specialty and license_number are required"
        }), 400



    result = service.create_profile(
        user_id,
        specialty,
        license_number,
        data.get("institution"),
        data.get("practice_area"),
        data.get("phone"),
        data.get("professional_email")
    )


    if not result["success"]:

        return jsonify(result), 400



    return jsonify(result), 201