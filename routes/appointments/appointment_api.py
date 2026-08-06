from flask import Blueprint, request, jsonify

from flask_jwt_extended import (
    jwt_required,
    get_jwt_identity
)

from security.permissions import role_required

from services.appointments.appointment_service import AppointmentService

from services.security_service.access_control_service import AccessControlService



appointment_bp = Blueprint(
    "appointment",
    __name__,
    url_prefix="/appointments"
)



service = AppointmentService()

access_control = AccessControlService()



# =====================================================
# CREATE APPOINTMENT (PATIENT)
# =====================================================

@appointment_bp.route(
    "/create",
    methods=["POST"]
)
@jwt_required()
@role_required("patient")
def create_appointment():


    data = request.get_json()


    if not data:

        return jsonify({

            "success": False,

            "message": "JSON body is required."

        }), 400



    user_id = get_jwt_identity()


    professional_id = data.get(
        "professional_id"
    )


    appointment_date = data.get(
        "appointment_date"
    )



    if not professional_id or not appointment_date:

        return jsonify({

            "success": False,

            "message": (
                "professional_id and appointment_date are required."
            )

        }), 400




    result = service.create_patient_appointment(

        user_id,

        professional_id,

        appointment_date,

        data.get("appointment_reason"),

        data.get("notes")

    )



    if not result["success"]:

        return jsonify(result), 400



    return jsonify(result), 201





# =====================================================
# MY APPOINTMENTS
# =====================================================

@appointment_bp.route(
    "/my",
    methods=["GET"]
)
@jwt_required()
def my_appointments():


    user_id = get_jwt_identity()



    # ADMIN

    if access_control.is_administrator(
        user_id
    ):

        appointments = (
            service.appointment_model
            .get_all()
        )


        return jsonify({

            "success": True,

            "appointments": [

                dict(item)

                for item in appointments

            ]

        }), 200




    # PATIENT

    patient = (
        service.patient_model
        .get_by_user_id(
            user_id
        )
    )


    if patient:


        appointments = (
            service.get_patient_appointments(
                patient["id"]
            )
        )


        return jsonify(
            appointments
        ), 200




    # PROFESSIONAL

    professional = (
        service.professional_model
        .get_by_user_id(
            user_id
        )
    )


    if professional:


        appointments = (
            service.get_professional_appointments(
                professional["id"]
            )
        )


        return jsonify(
            appointments
        ), 200




    return jsonify({

        "success": False,

        "message": "Profile not found."

    }), 404






# =====================================================
# ACCEPT APPOINTMENT
# =====================================================

@appointment_bp.route(
    "/<int:appointment_id>/accept",
    methods=["PUT"]
)
@jwt_required()
@role_required("professional")
def accept_appointment(
    appointment_id
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




    if appointment["professional_id"] != professional["id"]:

        return jsonify({

            "success": False,

            "message": "Access denied."

        }), 403




    result = service.accept_appointment(
        appointment_id
    )



    return jsonify(result), 200






# =====================================================
# CANCEL APPOINTMENT
# =====================================================

@appointment_bp.route(
    "/<int:appointment_id>/cancel",
    methods=["PUT"]
)
@jwt_required()
def cancel_appointment(
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





    result = service.cancel_appointment(
        appointment_id
    )



    return jsonify(result), 200






# =====================================================
# ADMIN - ALL APPOINTMENTS
# =====================================================

@appointment_bp.route(
    "/all",
    methods=["GET"]
)
@jwt_required()
@role_required("administrator")
def all_appointments():


    appointments = (
        service.appointment_model
        .get_all()
    )


    return jsonify({

        "success": True,

        "appointments": [

            dict(item)

            for item in appointments

        ]

    }), 200