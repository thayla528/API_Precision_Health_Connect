from flask import Blueprint, request, jsonify

from database.professionals.professional_entity_model import ProfessionalEntityModel
from services.security_service.access_control_service import AccessControlService

from services.patients.patient_professional_service import PatientProfessionalService

from flask_jwt_extended import jwt_required, get_jwt_identity

from security.permissions import role_required


patient_professional_bp = Blueprint(
    "patient_professional",
    __name__,
    url_prefix="/patient-professional"
)


service = PatientProfessionalService()

access_control = AccessControlService()


# =====================================================
# CREATE LINK
# =====================================================

# =====================================================
# CREATE LINK
# =====================================================

@patient_professional_bp.route(
    "/create",
    methods=["POST"]
)
@jwt_required()
def create_link():

    data = request.get_json()


    if not data:

        return jsonify({

            "message":
                "JSON body is required"

        }), 400


    patient_id = data.get(
        "patient_id"
    )

    professional_id = data.get(
        "professional_id"
    )


    if not patient_id or not professional_id:

        return jsonify({

            "message":
                "patient_id and professional_id are required"

        }), 400


    current_user_id = get_jwt_identity()


    allowed = access_control.can_access_professional(

        current_user_id,

        professional_id

    )


    if not allowed:

        return jsonify({

            "message":
                "Access denied."

        }), 403


    result = service.create_link(

        patient_id,

        professional_id

    )


    if not result["success"]:

        return jsonify(result), 400


    return jsonify(result), 201


# =====================================================
# GET PATIENTS OF PROFESSIONAL
# =====================================================

@patient_professional_bp.route(
    "/professional/<int:professional_id>/patients",
    methods=["GET"]
)
@jwt_required()
def get_professional_patients(
    professional_id
):

    current_user_id = get_jwt_identity()


    allowed = access_control.can_access_professional(

        current_user_id,

        professional_id

    )


    if not allowed:

        return jsonify({

            "message":
                "Access denied."

        }), 403


    result = service.get_professional_patients(

        professional_id

    )


    return jsonify(result), 200


# =====================================================
# GET PROFESSIONALS OF PATIENT
# =====================================================

@patient_professional_bp.route(
    "/patient/<int:patient_id>/professionals",
    methods=["GET"]
)
@jwt_required()
def get_patient_professionals(
    patient_id
):

    current_user_id = get_jwt_identity()


    allowed = access_control.can_access_patient(

        current_user_id,

        patient_id

    )


    if not allowed:

        return jsonify({

            "message":
                "Access denied."

        }), 403


    result = service.get_patient_professionals(

        patient_id

    )


    return jsonify(result), 200



# =====================================================
# SEARCH PATIENTS
# =====================================================

@patient_professional_bp.route(
    "/patients/search",
    methods=["GET"]
)
@jwt_required()
def search_patients():

    search = request.args.get(
        "search",
        ""
    ).strip()


    patients = service.search_patients(
        search
    )


    return jsonify({

        "success": True,

        "patients": [

            dict(patient)

            for patient in patients

        ]

    }), 200


# =====================================================
# GET PENDING REQUESTS OF PATIENT
# =====================================================

@patient_professional_bp.route(
    "/patient/requests",
    methods=["GET"]
)
@jwt_required()
def get_pending_requests():

    current_user_id = get_jwt_identity()

    patient = access_control.patient_model.get_by_user_id(
        current_user_id
    )

    if not patient:

        return jsonify({

            "message":
                "Patient not found."

        }), 404

    patient_id = patient["id"]

    result = service.get_pending_requests(
        patient_id
    )

    return jsonify(result), 200


# =====================================================
# APPROVE RELATIONSHIP
# =====================================================

@patient_professional_bp.route(
    "/<int:link_id>/approve",
    methods=["PUT"]
)
@jwt_required()
def approve_relationship(link_id):

    current_user_id = get_jwt_identity()

    relationship = (
        service.relationship_model
        .get_by_id(link_id)
    )

    if not relationship:

        return jsonify({

            "message":
                "Relationship not found."

        }), 404

    patient_id = relationship["patient_id"]

    allowed = access_control.can_access_patient(
        current_user_id,
        patient_id
    )

    if not allowed:

        return jsonify({

            "message":
                "Access denied."

        }), 403

    result = service.approve_relationship(
        link_id
    )

    if not result["success"]:

        return jsonify(result), 400

    return jsonify(result), 200


# =====================================================
# REJECT RELATIONSHIP
# =====================================================

@patient_professional_bp.route(
    "/<int:link_id>/reject",
    methods=["PUT"]
)
@jwt_required()
def reject_relationship(link_id):

    current_user_id = get_jwt_identity()

    relationship = (
        service.relationship_model
        .get_by_id(link_id)
    )

    if not relationship:

        return jsonify({

            "message":
                "Relationship not found."

        }), 404

    patient_id = relationship["patient_id"]

    allowed = access_control.can_access_patient(
        current_user_id,
        patient_id
    )

    if not allowed:

        return jsonify({

            "message":
                "Access denied."

        }), 403

    result = service.reject_relationship(
        link_id
    )

    if not result["success"]:

        return jsonify(result), 400

    return jsonify(result), 200

# =====================================================
# GET MY PATIENTS
# =====================================================

@patient_professional_bp.route(
    "/my-patients",
    methods=["GET"]
)
@jwt_required()
def get_my_patients():

    current_user_id = get_jwt_identity()

    professional = ProfessionalEntityModel.get_by_user_id(
        current_user_id
    )

    if not professional:

        return jsonify({

            "success": False,

            "message":
                "Professional not found."

        }), 404

    professional_id = professional["id"]

    result = service.get_professional_patients(

        professional_id

    )

    return jsonify(result), 200

# =====================================================
# DISABLE LINK
# =====================================================

@patient_professional_bp.route(
    "/<int:link_id>/disable",
    methods=["PUT"]
)
@jwt_required()
@role_required("administrator")
def disable_link(
    link_id
):

    result = service.deactivate_link(

        link_id

    )


    if not result["success"]:

        return jsonify(result), 404


    return jsonify(result), 200