from flask import Blueprint, request, jsonify

from flask_jwt_extended import (
    jwt_required,
    get_jwt_identity
)

from security.permissions import role_required

from services.clinical_records.clinical_record_service import ClinicalRecordService

from services.security_service.access_control_service import AccessControlService



clinical_record_bp = Blueprint(
    "clinical_record",
    __name__,
    url_prefix="/clinical-records"
)



service = ClinicalRecordService()

access_control = AccessControlService()



# =====================================================
# CREATE CLINICAL RECORD
# PROFESSIONAL ONLY
# =====================================================

@clinical_record_bp.route(
    "/create",
    methods=["POST"]
)
@jwt_required()
@role_required("professional")
def create_record():


    user_id = get_jwt_identity()



    professional = (
        service.professional_model
        .get_by_user_id(
            user_id
        )
    )


    if not professional:

        return jsonify({

            "success": False,

            "message": "Professional profile not found."

        }), 404





    data = request.get_json()



    if not data:

        return jsonify({

            "success": False,

            "message": "JSON body is required."

        }), 400




    appointment_id = data.get(
        "appointment_id"
    )


    if not appointment_id:

        return jsonify({

            "success": False,

            "message": "appointment_id is required."

        }), 400





    result = service.create_record(

        professional["id"],

        appointment_id,

        data.get("diagnosis"),

        data.get("treatment"),

        data.get("prescription"),

        data.get("notes")

    )



    if not result["success"]:

        return jsonify(result), 400



    return jsonify(result), 201





# =====================================================
# GET PATIENT RECORDS
# PATIENT / PROFESSIONAL LINKED / ADMIN
# =====================================================

@clinical_record_bp.route(
    "/patient/<int:patient_id>",
    methods=["GET"]
)
@jwt_required()
def get_patient_records(
        patient_id
):


    user_id = get_jwt_identity()



    allowed = False



    if access_control.is_administrator(
        user_id
    ):

        allowed = True



    elif access_control.can_access_patient(
        user_id,
        patient_id
    ):

        allowed = True



    if not allowed:

        return jsonify({

            "success": False,

            "message": "Access denied."

        }), 403





    result = service.get_patient_records(

        patient_id

    )



    return jsonify(result), 200






# =====================================================
# GET APPOINTMENT RECORDS
# ADMIN / PATIENT / PROFESSIONAL
# =====================================================

@clinical_record_bp.route(
    "/appointment/<int:appointment_id>",
    methods=["GET"]
)
@jwt_required()
def get_appointment_records(
        appointment_id
):


    user_id = get_jwt_identity()



    appointment = (
        service.appointment_model
        .get_by_id(
            appointment_id
        )
    )


    if not appointment:

        return jsonify({

            "success": False,

            "message": "Appointment not found."

        }), 404




    allowed = False



    if access_control.is_administrator(
        user_id
    ):

        allowed = True



    elif access_control.can_access_patient(

        user_id,

        appointment["patient_id"]

    ):

        allowed = True



    elif access_control.can_access_professional(

        user_id,

        appointment["professional_id"]

    ):

        allowed = True





    if not allowed:

        return jsonify({

            "success": False,

            "message": "Access denied."

        }), 403





    result = service.get_appointment_records(

        appointment_id

    )



    return jsonify(result), 200






# =====================================================
# ADMIN - ALL RECORDS
# =====================================================

@clinical_record_bp.route(
    "/all",
    methods=["GET"]
)
@jwt_required()
@role_required("administrator")
def get_all_records():



    result = service.get_all_records()



    return jsonify(result), 200