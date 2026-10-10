from database.prescriptions.prescription_model import PrescriptionModel

from database.appointments.appointment_model import AppointmentModel

from database.patients.patient_professional_model import PatientProfessionalModel

from database.patients.patient_entity_model import PatientEntityModel

from database.professionals.professional_entity_model import ProfessionalEntityModel

from services.audit.audit_service import AuditService


class PrescriptionService:

    def __init__(self):

        self.prescription_model = PrescriptionModel()

        self.appointment_model = AppointmentModel()

        self.relationship_model = PatientProfessionalModel()

        self.patient_model = PatientEntityModel()

        self.professional_model = ProfessionalEntityModel()

        self.audit_service = AuditService()



    # =====================================================
    # CREATE PRESCRIPTION
    # =====================================================

    def create_prescription(
            self,
            user_id,
            professional_id,
            patient_id,
            appointment_id=None,
            medication=None,
            dosage=None,
            frequency=None,
            duration=None,
            prescription_type=None,
            instructions=None
    ):

        # -------------------------------------------------
        # VERIFY PATIENT
        # -------------------------------------------------

        patient = (
            self.patient_model
            .get_by_id(
                patient_id
            )
        )


        if not patient:

            return {

                "success": False,

                "message": "Patient not found."

            }



        # -------------------------------------------------
        # VERIFY PROFESSIONAL
        # -------------------------------------------------

        professional = (
            self.professional_model
            .get_by_id(
                professional_id
            )
        )


        if not professional:

            return {

                "success": False,

                "message": "Professional not found."

            }



        # -------------------------------------------------
        # VERIFY PATIENT-PROFESSIONAL RELATIONSHIP
        # -------------------------------------------------

        relationship = (
            self.relationship_model
            .relationship_exists(
                patient_id,
                professional_id
            )
        )


        if not relationship:

            return {

                "success": False,

                "message":
                    "This patient is not linked to this professional."

            }



        # -------------------------------------------------
        # VERIFY APPOINTMENT
        # -------------------------------------------------

        if appointment_id:

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



            # -------------------------------------------------
            # VERIFY APPOINTMENT BELONGS TO PROFESSIONAL
            # -------------------------------------------------

            if appointment["professional_id"] != professional_id:

                return {

                    "success": False,

                    "message":
                        "This appointment does not belong to this professional."

                }



            # -------------------------------------------------
            # VERIFY APPOINTMENT BELONGS TO PATIENT
            # -------------------------------------------------

            if appointment["patient_id"] != patient_id:

                return {

                    "success": False,

                    "message":
                        "This appointment does not belong to this patient."

                }



        # -------------------------------------------------
        # VERIFY MEDICATION
        # -------------------------------------------------

        if not medication:

            return {

                "success": False,

                "message": "Medication is required."

            }



        # -------------------------------------------------
        # CREATE PRESCRIPTION
        # -------------------------------------------------

        prescription_id = (
            self.prescription_model
            .create(

                patient_id,

                professional_id,

                appointment_id,

                medication,

                dosage,

                frequency,

                duration,

                prescription_type,

                instructions,

                "pending"

            )
        )



        # -------------------------------------------------
        # AUDIT LOG
        # -------------------------------------------------

        self.audit_service.register(

            user_id,

            "CREATE",

            "prescriptions",

            prescription_id,

            None,

            {

                "patient_id": patient_id,

                "professional_id": professional_id,

                "appointment_id": appointment_id,

                "medication": medication,

                "dosage": dosage,

                "frequency": frequency,

                "duration": duration,

                "prescription_type": prescription_type,

                "instructions": instructions,

                "status": "pending"

            }

        )



        return {

            "success": True,

            "message": "Prescription created successfully.",

            "prescription_id": prescription_id

        }



    # =====================================================
    # GET PRESCRIPTION BY ID
    # =====================================================

    def get_prescription(
            self,
            prescription_id
    ):

        prescription = (
            self.prescription_model
            .get_by_id(
                prescription_id
            )
        )


        if not prescription:

            return {

                "success": False,

                "message": "Prescription not found."

            }


        return {

            "success": True,

            "prescription": dict(prescription)

        }



    # =====================================================
    # GET PATIENT PRESCRIPTIONS
    # =====================================================

    def get_patient_prescriptions(
            self,
            patient_id
    ):

        prescriptions = (
            self.prescription_model
            .get_by_patient(
                patient_id
            )
        )


        return {

            "success": True,

            "prescriptions": [

                dict(prescription)

                for prescription in prescriptions

            ]

        }



    # =====================================================
    # GET PROFESSIONAL PRESCRIPTIONS
    # =====================================================

    def get_professional_prescriptions(
            self,
            professional_id
    ):

        prescriptions = (
            self.prescription_model
            .get_by_professional(
                professional_id
            )
        )


        return {

            "success": True,

            "prescriptions": [

                dict(prescription)

                for prescription in prescriptions

            ]

        }



    # =====================================================
    # GET APPOINTMENT PRESCRIPTIONS
    # =====================================================

    def get_appointment_prescriptions(
            self,
            appointment_id
    ):

        prescriptions = (
            self.prescription_model
            .get_by_appointment(
                appointment_id
            )
        )


        return {

            "success": True,

            "prescriptions": [

                dict(prescription)

                for prescription in prescriptions

            ]

        }



    # =====================================================
    # GET ALL PRESCRIPTIONS
    # =====================================================

    def get_all_prescriptions(self):

        prescriptions = (
            self.prescription_model
            .get_all()
        )


        return {

            "success": True,

            "prescriptions": [

                dict(prescription)

                for prescription in prescriptions

            ]

        }



    # =====================================================
    # UPDATE PRESCRIPTION
    # =====================================================

    def update_prescription(
            self,
            user_id,
            prescription_id,
            medication=None,
            dosage=None,
            frequency=None,
            duration=None,
            prescription_type=None,
            instructions=None,
            status=None
    ):

        prescription = (
            self.prescription_model
            .get_by_id(
                prescription_id
            )
        )


        if not prescription:

            return {

                "success": False,

                "message": "Prescription not found."

            }


        old_data = dict(prescription)



        # -------------------------------------------------
        # KEEP CURRENT VALUES WHEN NOT PROVIDED
        # -------------------------------------------------

        if medication is None:

            medication = prescription["medication"]


        if dosage is None:

            dosage = prescription["dosage"]


        if frequency is None:

            frequency = prescription["frequency"]


        if duration is None:

            duration = prescription["duration"]


        if prescription_type is None:

            prescription_type = prescription["prescription_type"]


        if instructions is None:

            instructions = prescription["instructions"]


        if status is None:

            status = prescription["status"]



        # -------------------------------------------------
        # UPDATE
        # -------------------------------------------------

        updated = (
            self.prescription_model
            .update(

                prescription_id,

                medication,

                dosage,

                frequency,

                duration,

                prescription_type,

                instructions,

                status

            )
        )


        if updated == 0:

            return {

                "success": False,

                "message": "Prescription was not updated."

            }



        # -------------------------------------------------
        # NEW DATA FOR AUDIT
        # -------------------------------------------------

        new_data = {

            "medication": medication,

            "dosage": dosage,

            "frequency": frequency,

            "duration": duration,

            "prescription_type": prescription_type,

            "instructions": instructions,

            "status": status

        }



        # -------------------------------------------------
        # AUDIT LOG
        # -------------------------------------------------

        self.audit_service.register(

            user_id,

            "UPDATE",

            "prescriptions",

            prescription_id,

            old_data,

            new_data

        )



        return {

            "success": True,

            "message": "Prescription updated successfully."

        }