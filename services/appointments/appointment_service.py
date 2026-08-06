from database.appointments.appointment_model import AppointmentModel

from database.patients.patient_entity_model import PatientEntityModel

from database.professionals.professional_entity_model import ProfessionalEntityModel

from database.patients.patient_professional_model import PatientProfessionalModel

from database.users.user_model import UserModel

from services.notifications.notification_service import NotificationService



class AppointmentService:
    ALLOWED_STATUS = [
        "pending",
        "scheduled",
        "cancelled",
        "completed"
    ]

    def __init__(self):

        self.user_model = UserModel()

        self.appointment_model = AppointmentModel()

        self.patient_model = PatientEntityModel()

        self.professional_model = ProfessionalEntityModel()

        self.relationship_model = PatientProfessionalModel()

        self.notification_service = NotificationService()


    # =====================================================
    # CREATE APPOINTMENT BY PATIENT
    # =====================================================

    def create_patient_appointment(
            self,
            user_id,
            professional_id,
            appointment_date,
            appointment_reason=None,
            notes=None
    ):


        patient = self.patient_model.get_by_user_id(
            user_id
        )


        if not patient:

            return {
                "success": False,
                "message": "Patient profile not found."
            }




        professional = self.professional_model.get_by_id(
            professional_id
        )


        if not professional:

            return {
                "success": False,
                "message": "Professional not found."
            }




        relationship = (
            self.relationship_model
            .relationship_exists(
                patient["id"],
                professional_id
            )
        )


        if not relationship:

            return {
                "success": False,
                "message": "Patient is not linked to this professional."
            }

        existing = (
            self.appointment_model
            .appointment_exists(
                patient["id"],
                professional_id,
                appointment_date
            )
        )

        if existing:
            return {

                "success": False,

                "message": "Appointment already exists for this date."

            }






        appointment_id = (
            self.appointment_model
            .create(
                patient["id"],
                professional_id,
                appointment_date,
                appointment_reason,
                None,
                notes,
                "pending"
            )
        )

        professional_user = self.user_model.get_by_id(
            professional["user_id"]
        )

        self.notification_service.create_notification(

            professional_user["id"],

            "New appointment request",

            "A patient requested a new appointment.",

            "appointment"

        )



        return {

            "success": True,

            "message": "Appointment request created successfully.",

            "appointment_id": appointment_id

        }






    # =====================================================
    # GET PATIENT APPOINTMENTS
    # =====================================================

    def get_patient_appointments(
            self,
            patient_id
    ):


        appointments = (
            self.appointment_model
            .get_by_patient(
                patient_id
            )
        )


        return {

            "success": True,

            "appointments": [

                dict(item)

                for item in appointments

            ]

        }





    # =====================================================
    # GET PROFESSIONAL APPOINTMENTS
    # =====================================================

    def get_professional_appointments(
            self,
            professional_id
    ):


        appointments = (
            self.appointment_model
            .get_by_professional(
                professional_id
            )
        )


        return {

            "success": True,

            "appointments": [

                dict(item)

                for item in appointments

            ]

        }




    # =====================================================
    # GET ALL APPOINTMENTS
    # =====================================================

    def get_all_appointments(self):


        appointments = (
            self.appointment_model
            .get_all()
        )


        return {

            "success": True,

            "appointments": [

                dict(item)

                for item in appointments

            ]

        }





    # =====================================================
    # ACCEPT APPOINTMENT
    # =====================================================

    def accept_appointment(
            self,
            appointment_id
    ):


        appointment = (
            self.appointment_model
            .get_by_id(
                appointment_id
            )
        )


        if not appointment:

            return {

                "success": False,

                "message": "Appointment not found."

            }



        if appointment["status"] != "pending":

            return {

                "success": False,

                "message": "Only pending appointments can be accepted."

            }




        updated = (
            self.appointment_model
            .update_status(
                appointment_id,
                "scheduled"
            )
        )

        patient = self.patient_model.get_by_id(
            appointment["patient_id"]
        )

        self.notification_service.create_notification(

            patient["user_id"],

            "Appointment confirmed",

            "Your appointment was accepted by the professional.",

            "appointment"

        )



        if updated == 0:

            return {

                "success": False,

                "message": "Appointment status was not updated."

            }




        return {

            "success": True,

            "message": "Appointment accepted successfully."

        }




    # =====================================================
    # CANCEL APPOINTMENT
    # =====================================================

    def cancel_appointment(
            self,
            appointment_id
    ):


        appointment = (
            self.appointment_model
            .get_by_id(
                appointment_id
            )
        )


        if not appointment:

            return {

                "success": False,

                "message": "Appointment not found."

            }

        if appointment["status"] in [
            "cancelled",
            "completed"
        ]:
            return {

                "success": False,

                "message": "Appointment cannot be cancelled."

            }




        updated = (
            self.appointment_model
            .update_status(
                appointment_id,
                "cancelled"
            )
        )

        patient = self.patient_model.get_by_id(
            appointment["patient_id"]
        )

        professional = self.professional_model.get_by_id(
            appointment["professional_id"]
        )

        self.notification_service.create_notification(

            patient["user_id"],

            "Appointment cancelled",

            "Your appointment was cancelled.",

            "appointment"

        )

        self.notification_service.create_notification(

            professional["user_id"],

            "Appointment cancelled",

            "An appointment was cancelled.",

            "appointment"

        )



        if updated == 0:

            return {

                "success": False,

                "message": "Appointment was not cancelled."

            }




        return {

            "success": True,

            "message": "Appointment cancelled successfully."

        }





    # =====================================================
    # UPDATE STATUS ADMIN
    # =====================================================

    def update_status(
            self,
            appointment_id,
            status
    ):
        if status not in self.ALLOWED_STATUS:
            return {

                "success": False,

                "message": "Invalid appointment status."

            }


        appointment = (
            self.appointment_model
            .get_by_id(
                appointment_id
            )
        )


        if not appointment:

            return {

                "success": False,

                "message": "Appointment not found."

            }




        updated = (
            self.appointment_model
            .update_status(
                appointment_id,
                status
            )
        )



        if updated == 0:

            return {

                "success": False,

                "message": "Status not updated."

            }




        return {

            "success": True,

            "message": "Appointment status updated successfully."

        }