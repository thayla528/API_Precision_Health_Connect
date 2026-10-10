from flask import Blueprint, request, jsonify

from flask_jwt_extended import (
    jwt_required,
    get_jwt_identity
)

from security.permissions import role_required

from services.prescription.prescription_service import PrescriptionService

from services.security_service.access_control_service import AccessControlService


prescription_bp = Blueprint(
    "prescription",
    __name__,
    url_prefix="/prescriptions"
)

service = PrescriptionService()

access_control = AccessControlService()


# =====================================================
# CREATE PRESCRIPTION
# PROFESSIONAL ONLY
# =====================================================

@prescription_bp.route(
    "/create",
    methods=["POST"]
)
@jwt_required()
@role_required("professional")
def create_prescription():

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

    patient_id = data.get(
        "patient_id"
    )

    medication = data.get(
        "medication"
    )

    if not patient_id:

        return jsonify({

            "success": False,

            "message": "patient_id is required."

        }), 400

    if not medication:

        return jsonify({

            "success": False,

            "message": "medication is required."

        }), 400

    result = service.create_prescription(

        user_id,

        professional["id"],

        patient_id,

        data.get("appointment_id"),

        medication,

        data.get("dosage"),

        data.get("frequency"),

        data.get("duration"),

        data.get("prescription_type"),

        data.get("instructions")

    )

    if not result["success"]:

        return jsonify(result), 400

    return jsonify(result), 201


# =====================================================
# GET MY PRESCRIPTIONS
# PROFESSIONAL ONLY
# =====================================================

@prescription_bp.route(
    "/my",
    methods=["GET"]
)
@jwt_required()
@role_required("professional")
def get_my_prescriptions():

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

    result = (
        service.get_professional_prescriptions(
            professional["id"]
        )
    )

    return jsonify(result), 200


# =====================================================
# GET PRESCRIPTION
# ADMIN / PATIENT / PROFESSIONAL
# =====================================================

@prescription_bp.route(
    "/<int:prescription_id>",
    methods=["GET"]
)
@jwt_required()
def get_prescription(
        prescription_id
):

    user_id = get_jwt_identity()

    result = service.get_prescription(
        prescription_id
    )

    if not result["success"]:

        return jsonify(result), 404

    prescription = result["prescription"]

    allowed = False

    # -------------------------------------------------
    # ADMIN
    # -------------------------------------------------

    if access_control.is_administrator(
        user_id
    ):

        allowed = True

    # -------------------------------------------------
    # PATIENT
    # -------------------------------------------------

    elif access_control.can_access_patient(
        user_id,
        prescription["patient_id"]
    ):

        allowed = True

    # -------------------------------------------------
    # PROFESSIONAL
    # -------------------------------------------------

    else:

        professional = (
            service.professional_model
            .get_by_user_id(
                user_id
            )
        )

        if professional:

            if professional["id"] == prescription["professional_id"]:

                allowed = True

    if not allowed:

        return jsonify({

            "success": False,

            "message": "Access denied."

        }), 403

    return jsonify(result), 200


# =====================================================
# GET PATIENT PRESCRIPTIONS
# ADMIN / PATIENT / PROFESSIONAL
# =====================================================

@prescription_bp.route(
    "/patient/<int:patient_id>",
    methods=["GET"]
)
@jwt_required()
def get_patient_prescriptions(
        patient_id
):

    user_id = get_jwt_identity()

    allowed = False

    # -------------------------------------------------
    # ADMIN
    # -------------------------------------------------

    if access_control.is_administrator(
        user_id
    ):

        allowed = True

    # -------------------------------------------------
    # PATIENT
    # -------------------------------------------------

    elif access_control.can_access_patient(
        user_id,
        patient_id
    ):

        allowed = True

    # -------------------------------------------------
    # PROFESSIONAL
    # -------------------------------------------------

    else:

        professional = (
            service.professional_model
            .get_by_user_id(
                user_id
            )
        )

        if professional:

            relationship = (
                service.relationship_model
                .relationship_exists(

                    patient_id,

                    professional["id"]

                )
            )

            if relationship:

                allowed = True

    if not allowed:

        return jsonify({

            "success": False,

            "message": "Access denied."

        }), 403

    result = (
        service.get_patient_prescriptions(
            patient_id
        )
    )

    return jsonify(result), 200


# =====================================================
# GET APPOINTMENT PRESCRIPTIONS
# ADMIN / PATIENT / PROFESSIONAL
# =====================================================

@prescription_bp.route(
    "/appointment/<int:appointment_id>",
    methods=["GET"]
)
@jwt_required()
def get_appointment_prescriptions(
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

    # -------------------------------------------------
    # ADMIN
    # -------------------------------------------------

    if access_control.is_administrator(
        user_id
    ):

        allowed = True

    # -------------------------------------------------
    # PATIENT
    # -------------------------------------------------

    elif access_control.can_access_patient(
        user_id,
        appointment["patient_id"]
    ):

        allowed = True

    # -------------------------------------------------
    # PROFESSIONAL
    # -------------------------------------------------

    else:

        professional = (
            service.professional_model
            .get_by_user_id(
                user_id
            )
        )

        if professional:

            if professional["id"] == appointment["professional_id"]:

                allowed = True

    if not allowed:

        return jsonify({

            "success": False,

            "message": "Access denied."

        }), 403

    result = (
        service.get_appointment_prescriptions(
            appointment_id
        )
    )

    return jsonify(result), 200


# =====================================================
# GET ALL PRESCRIPTIONS
# ADMIN ONLY
# =====================================================

@prescription_bp.route(
    "/all",
    methods=["GET"]
)
@jwt_required()
@role_required("administrator")
def get_all_prescriptions():

    result = (
        service.get_all_prescriptions()
    )

    return jsonify(result), 200


# =====================================================
# UPDATE PRESCRIPTION
# PROFESSIONAL ONLY
# =====================================================

@prescription_bp.route(
    "/<int:prescription_id>",
    methods=["PUT"]
)
@jwt_required()
@role_required("professional")
def update_prescription(
        prescription_id
):

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

    prescription = (
        service.prescription_model
        .get_by_id(
            prescription_id
        )
    )

    if not prescription:

        return jsonify({

            "success": False,

            "message": "Prescription not found."

        }), 404

    if prescription["professional_id"] != professional["id"]:

        return jsonify({

            "success": False,

            "message": "You cannot update this prescription."

        }), 403

    data = request.get_json()

    if not data:

        return jsonify({

            "success": False,

            "message": "JSON body is required."

        }), 400

    result = service.update_prescription(

        user_id,

        prescription_id,

        data.get("medication"),

        data.get("dosage"),

        data.get("frequency"),

        data.get("duration"),

        data.get("prescription_type"),

        data.get("instructions"),

        data.get("status")

    )

    if not result["success"]:

        return jsonify(result), 400

    return jsonify(result), 200