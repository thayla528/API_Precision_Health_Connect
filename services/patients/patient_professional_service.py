from database.patients.patient_professional_model import PatientProfessionalModel
from database.professionals.professional_entity_model import ProfessionalEntityModel
from database.patients.patient_entity_model import PatientEntityModel


class PatientProfessionalService:

    def __init__(self):
        self.relationship_model = PatientProfessionalModel()
        self.professional_model = ProfessionalEntityModel()
        self.patient_model = PatientEntityModel()


    def create_link(self, patient_id, professional_id):

        patient = self.patient_model.get_by_id(
            patient_id
        )

        if not patient:
            return {
                "success": False,
                "message": "Patient not found."
            }


        professional = self.professional_model.get_by_id(
            professional_id
        )

        if not professional:
            return {
                "success": False,
                "message": "Professional not found."
            }


        relationship = self.relationship_model.relationship_exists(
            patient_id,
            professional_id
        )


        if relationship:
            return {
                "success": False,
                "message": "Relationship already exists."
            }


        relationship_id = self.relationship_model.create(
            patient_id,
            professional_id
        )


        return {
            "success": True,
            "message": "Relationship created successfully.",
            "relationship_id": relationship_id
        }

    def get_patient_professionals(self, patient_id):

        relationships = (
            self.relationship_model
            .get_by_patient(patient_id)
        )

        return {
            "success": True,
            "relationships": [
                dict(item)
                for item in relationships
            ]
        }

    def get_professional_patients(self, professional_id):

        relationships = (
            self.relationship_model
            .get_by_professional(professional_id)
        )

        return {
            "success": True,
            "relationships": [
                dict(item)
                for item in relationships
            ]
        }


    def deactivate_link(self, relationship_id):

        rows_updated = (
            self.relationship_model
            .deactivate(relationship_id)
        )


        if rows_updated == 0:
            return {
                "success": False,
                "message": "Relationship not found."
            }


        return {
            "success": True,
            "message": "Relationship deactivated successfully."
        }