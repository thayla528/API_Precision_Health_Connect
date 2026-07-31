from flask import Blueprint, request, jsonify

from flask_jwt_extended import jwt_required, get_jwt_identity

from services.patient_professional_service import PatientProfessionalService

from services.user_service import UserService

from security.permissions import role_required


patient_professional_bp = Blueprint(
    "patient_professional",
    __name__,
    url_prefix="/patient-professional"
)



# =====================================================
# CREATE LINK
# =====================================================

@patient_professional_bp.route("/create", methods=["POST"])
@jwt_required()
@role_required("admin")
def create_link():

    data = request.get_json()

    patient_id = data.get("patient_id")
    professional_id = data.get("professional_id")


    if not patient_id or not professional_id:
        return jsonify({
            "message": "patient_id and professional_id are required"
        }), 400



    relationship = PatientProfessionalService.create_link(
        patient_id,
        professional_id
    )


    if not relationship:
        return jsonify({
            "message": "Relationship already exists"
        }), 400



    return jsonify({
        "message": "Patient linked to professional successfully",
        "relationship": {
            "id": relationship.id,
            "patient_id": relationship.patient_id,
            "professional_id": relationship.professional_id
        }
    }), 201




# =====================================================
# GET PATIENT PROFESSIONALS
# =====================================================

@patient_professional_bp.route(
    "/patient/<int:patient_id>/professionals",
    methods=["GET"]
)
@jwt_required()
def get_patient_professionals(patient_id):

    professionals = (
        PatientProfessionalService
        .get_patient_professionals(patient_id)
    )


    return jsonify([
        {
            "id": item.id,
            "professional_id": item.professional_id,
            "status": item.status
        }
        for item in professionals
    ]), 200





# =====================================================
# GET PROFESSIONAL PATIENTS
# =====================================================

@patient_professional_bp.route(
    "/professional/<int:professional_id>/patients",
    methods=["GET"]
)
@jwt_required()
def get_professional_patients(professional_id):

    patients = (
        PatientProfessionalService
        .get_professional_patients(professional_id)
    )


    return jsonify([
        {
            "id": item.id,
            "patient_id": item.patient_id,
            "status": item.status
        }
        for item in patients
    ]), 200





# =====================================================
# DISABLE LINK
# =====================================================

@patient_professional_bp.route(
    "/<int:link_id>/disable",
    methods=["PUT"]
)
@jwt_required()
@role_required("admin")
def disable_link(link_id):

    result = (
        PatientProfessionalService
        .deactivate_link(link_id)
    )


    if not result:
        return jsonify({
            "message": "Relationship not found"
        }), 404



    return jsonify({
        "message": "Relationship disabled successfully"
    }), 200