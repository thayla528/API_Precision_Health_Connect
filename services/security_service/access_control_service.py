from database.users.user_model import UserModel
from database.patients.patient_entity_model import PatientEntityModel
from database.professionals.professional_entity_model import ProfessionalEntityModel


class AccessControlService:


    def __init__(self):

        self.user_model = UserModel()
        self.patient_model = PatientEntityModel()
        self.professional_model = ProfessionalEntityModel()



    def has_role(self, user_id, role):

        user = self.user_model.get_by_id(
            user_id
        )


        if not user:
            return False


        return user["role"] == role



    def is_administrator(self, user_id):

        return self.has_role(
            user_id,
            "administrator"
        )



    def can_access_patient(
            self,
            user_id,
            patient_id
    ):

        if self.is_administrator(user_id):
            return True


        patient = self.patient_model.get_by_id(
            patient_id
        )


        if not patient:
            return False


        return int(patient["user_id"]) == int(user_id)



    def can_access_professional(
            self,
            user_id,
            professional_id
    ):

        if self.is_administrator(user_id):
            return True


        professional = self.professional_model.get_by_id(
            professional_id
        )


        if not professional:
            return False


        return int(professional["user_id"]) == int(user_id)