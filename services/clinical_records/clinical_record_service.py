from database.clinical_record.clinical_record_model import ClinicalRecordModel

from database.appointments.appointment_model import AppointmentModel

from database.patients.patient_professional_model import PatientProfessionalModel

from database.patients.patient_entity_model import PatientEntityModel

from database.professionals.professional_entity_model import ProfessionalEntityModel
from services.audit.audit_service import AuditService


class ClinicalRecordService:

    def __init__(self):

        self.record_model = ClinicalRecordModel()

        self.appointment_model = AppointmentModel()

        self.relationship_model = PatientProfessionalModel()

        self.patient_model = PatientEntityModel()

        self.professional_model = ProfessionalEntityModel()

        self.audit_service = AuditService()



    # =====================================================
    # CREATE CLINICAL RECORD
    # =====================================================

    def create_record(
            self,
            professional_id,
            appointment_id,
            diagnosis=None,
            treatment=None,
            prescription=None,
            notes=None
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




        if appointment["professional_id"] != professional_id:

            return {

                "success": False,

                "message": "This appointment does not belong to this professional."

            }





        if appointment["status"] != "scheduled":

            return {

                "success": False,

                "message": "Only scheduled appointments can receive clinical records."

            }





        record_id = (
            self.record_model
            .create(

                appointment_id,

                diagnosis,

                treatment,

                prescription,

                notes

            )
        )



        return {

            "success": True,

            "message": "Clinical record created successfully.",

            "record_id": record_id

        }





    # =====================================================
    # GET PATIENT RECORDS
    # =====================================================

    def get_patient_records(
            self,
            patient_id
    ):


        records = (
            self.record_model
            .get_by_patient(
                patient_id
            )
        )


        return {


            "success": True,


            "records": [


                dict(record)

                for record in records


            ]

        }





    # =====================================================
    # GET APPOINTMENT RECORDS
    # =====================================================

    def get_appointment_records(
            self,
            appointment_id
    ):


        records = (
            self.record_model
            .get_by_appointment(
                appointment_id
            )
        )


        return {


            "success": True,


            "records": [


                dict(record)

                for record in records


            ]

        }





    # =====================================================
    # GET ALL RECORDS ADMIN
    # =====================================================

    def get_all_records(self):


        records = (
            self.record_model
            .get_all()
        )


        return {


            "success": True,


            "records": [


                dict(record)

                for record in records


            ]

        }

    # =====================================================
    # UPDATE CLINICAL RECORD
    # =====================================================

    def update_record(
            self,
            user_id,
            record_id,
            diagnosis=None,
            treatment=None,
            prescription=None,
            notes=None
    ):


        record = (
            self.record_model
            .get_by_id(
                record_id
            )
        )


        if not record:

            return {

                "success": False,

                "message": "Clinical record not found."

            }

        old_data = dict(record)




        updated = (
            self.record_model
            .update(

                record_id,

                diagnosis,

                treatment,

                prescription,

                notes

            )
        )



        if updated == 0:

            return {

                "success": False,

                "message": "Clinical record was not updated."

            }

        new_data = {

            "diagnosis": diagnosis,

            "treatment": treatment,

            "prescription": prescription,

            "notes": notes

        }

        self.audit_service.register(

            user_id,

            "UPDATE",

            "clinical_records",

            record_id,

            old_data,

            new_data

        )




        return {

            "success": True,

            "message": "Clinical record updated successfully."

        }