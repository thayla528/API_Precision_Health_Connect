from database.users.user_model import UserModel
from database.invitations.invitation_model import InvitationModel

from werkzeug.security import generate_password_hash

from database.patients.patient_entity_model import PatientEntityModel
from database.professionals.professional_entity_model import ProfessionalEntityModel
from database.administrators.administrator_entity_model import AdministratorEntityModel

from services.audit.audit_service import AuditService

class UserService:


    def __init__(self):

        self.audit_service = AuditService()

        self.user_model = UserModel()

        self.invitation_model = InvitationModel()

        self.patient_model = PatientEntityModel()

        self.professional_model = ProfessionalEntityModel()

        self.administrator_model = AdministratorEntityModel()



    def register_user(
            self,
            invitation_code,
            password,
            profile_photo
    ):


        if not password:

            return {
                "success": False,
                "message": "Password is required."
            }



        # Buscar convite

        invitation = self.invitation_model.get_by_code(
            invitation_code
        )


        if not invitation:

            return {
                "success": False,
                "message": "Invalid invitation code."
            }



        # Verificar convite usado

        if invitation["used"] == 1:

            return {
                "success": False,
                "message": "Invitation already used."
            }



        # Verificar aprovação

        if invitation["status"] != "approved":

            return {
                "success": False,
                "message": "Invitation is not approved."
            }




        # Verificar usuário existente

        existing_user = self.user_model.get_by_email(
            invitation["email"]
        )


        if existing_user:

            return {
                "success": False,
                "message": "User already exists."
            }




        # Criptografar senha

        hashed_password = generate_password_hash(
            password
        )




        # Criar usuário

        user_id = self.user_model.create(

            invitation["id"],

            invitation["full_name"],

            invitation["email"],

            hashed_password,

            invitation["profile_type"],

            profile_photo

        )




        # Criar entidade correspondente

        if invitation["profile_type"] == "patient":


            self.patient_model.create(
                user_id
            )



        elif invitation["profile_type"] == "professional":


            self.professional_model.create(
                user_id
            )



        elif invitation["profile_type"] == "administrator":


            self.administrator_model.create(
                user_id
            )





        # Bloquear reutilização do convite

        self.invitation_model.mark_as_used(

            invitation["id"]

        )




        return {

            "success": True,

            "message": "User created successfully.",

            "user_id": user_id

        }

    def deactivate_user(
            self,
            admin_id,
            user_id
    ):

        user = self.user_model.get_by_id(user_id)

        if not user:
            return {

                "success": False,

                "message": "User not found."

            }

        old_data = {

            "active": user["active"]

        }

        updated = self.user_model.deactivate(
            user_id
        )

        if updated == 0:
            return {

                "success": False,

                "message": "User was not deactivated."

            }

        new_data = {

            "active": 0

        }

        self.audit_service.register(

            admin_id,

            "SOFT_DELETE",

            "users",

            user_id,

            old_data,

            new_data

        )

        return {

            "success": True,

            "message": "User deactivated successfully."

        }