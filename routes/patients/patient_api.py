from flask import Blueprint, jsonify

from services.patients.patient_service import PatientService


patient_api_bp = Blueprint(
    "patient_api_bp",
    __name__
)


patient_service = PatientService()



@patient_api_bp.route(
    "/api/patient/dashboard/<int:user_id>",
    methods=["GET"]
)
def patient_dashboard(user_id):

    result = patient_service.get_dashboard(
        user_id
    )

    return jsonify(result), 200



@patient_api_bp.route(
    "/api/patient/profile/<int:user_id>",
    methods=["GET"]
)
def patient_profile(user_id):

    result = patient_service.get_profile(
        user_id
    )

    return jsonify({
        "profile": result
    }), 200