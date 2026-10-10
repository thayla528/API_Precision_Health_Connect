from database.users.user_model import UserModel
from database.invitations.invitation_model import InvitationModel

from werkzeug.security import generate_password_hash

from database.patients.patient_entity_model import PatientEntityModel
from database.professionals.professional_entity_model import ProfessionalEntityModel
from database.administrators.administrator_entity_model import AdministratorEntityModel

from services.email.email_service import EmailService
import secrets

from services.audit.audit_service import AuditService

class UserService:


    def __init__(self):

        self.audit_service = AuditService()

        self.email_service = EmailService()

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

    def create_administrator(
            self,
            admin_id,
            full_name,
            email,
            profile_photo=None,
            phone=None
    ):

        # =====================================================
        # VALIDAR DADOS
        # =====================================================

        if not full_name or not full_name.strip():
            return {
                "success": False,
                "message": "Full name is required."
            }

        if not email or not email.strip():
            return {
                "success": False,
                "message": "Email is required."
            }

        full_name = full_name.strip()
        email = email.strip().lower()

        # =====================================================
        # VERIFICAR USUÁRIO EXISTENTE
        # =====================================================

        existing_user = self.user_model.get_by_email(email)

        if existing_user:
            return {
                "success": False,
                "message": "User already exists."
            }

        # =====================================================
        # CRIAR SOLICITAÇÃO DE CONVITE
        # =====================================================

        try:

            invitation_id = self.invitation_model.create(

                full_name=full_name,

                email=email,

                phone=phone,

                birth_date=None,

                profile_type="administrator",

                interest_reason=
                "Administrator created by administrator panel"

            )

        except Exception as e:

            print(
                "Erro ao criar convite:",
                e,
                flush=True
            )

            return {
                "success": False,
                "message": "Não foi possível criar o convite."
            }

        # =====================================================
        # GERAR CÓDIGO DO CONVITE
        # =====================================================

        invitation_code = secrets.token_hex(4)

        # =====================================================
        # APROVAR CONVITE
        # =====================================================

        try:

            self.invitation_model.approve(

                invitation_id,

                invitation_code,

                admin_id

            )

        except Exception as e:

            print(
                "Erro ao aprovar convite:",
                e,
                flush=True
            )

            return {
                "success": False,
                "message": "Não foi possível aprovar o convite."
            }

        # =====================================================
        # REGISTRAR AUDITORIA
        # =====================================================

        try:

            self.audit_service.register(

                admin_id,

                "CREATE_ADMINISTRATOR",

                "invitations",

                invitation_id,

                None,

                {
                    "status": "approved",
                    "full_name": full_name,
                    "email": email,
                    "profile_type": "administrator"
                }

            )

        except Exception as e:

            print(
                "Erro ao registrar auditoria:",
                e,
                flush=True
            )

            # O convite continua válido.
            # O erro de auditoria não impede o envio do e-mail.

        # =====================================================
        # ENVIAR E-MAIL
        # =====================================================

        try:

            email_sent = self.email_service.send_email(

                recipient=email,

                subject=
                "Convite de administrador - Precision Health Connect",

                message=f"""

                <h2>Olá, {full_name}!</h2>

                <p>
                    Você foi convidado para fazer parte da equipe
                    administrativa do
                    <strong>Precision Health Connect</strong>.
                </p>

                <p>
                    Para finalizar seu cadastro, utilize o código
                    de convite abaixo:
                </p>

                <div style="
                    margin: 25px 0;
                    padding: 20px;
                    text-align: center;
                    background-color: #f5f7f9;
                    border-radius: 10px;
                ">

                    <strong style="
                        font-size: 28px;
                        letter-spacing: 4px;
                    ">
                        {invitation_code}
                    </strong>

                </div>

                <p>
                    Utilize esse código na página de finalização
                    do cadastro.
                </p>

                <p>
                    Durante a finalização, você poderá definir
                    sua senha de acesso.
                </p>

                <p>
                    Atenciosamente,<br>
                    Equipe Precision Health Connect.
                </p>

                """

            )

        except Exception as e:

            print(
                "Erro ao enviar e-mail:",
                e,
                flush=True
            )

            email_sent = False

        # =====================================================
        # VERIFICAR ENVIO DO E-MAIL
        # =====================================================

        if not email_sent:
            return {

                "success": False,

                "message":
                    "Convite criado, mas não foi possível enviar o e-mail.",

                "invitation_id":
                    invitation_id,

                "email_sent":
                    False

            }

        # =====================================================
        # SUCESSO
        # =====================================================

        return {

            "success": True,

            "message":
                "Administrator invitation created successfully. Email sent.",

            "invitation_id":
                invitation_id,

            "email":
                email,

            "email_sent":
                True

        }



    def update_administrator(
            self,
            administrator_id,
            full_name,
            email,
            password=None,
            profile_photo=None,
            phone=None
    ):

        administrator = self.administrator_model.get_by_id(
            administrator_id
        )

        if not administrator:
            return {
                "success": False,
                "message": "Administrator not found."
            }

        user_id = administrator["user_id"]

        user = self.user_model.get_by_id(
            user_id
        )

        if not user:
            return {
                "success": False,
                "message": "User not found."
            }

        if not full_name:
            return {
                "success": False,
                "message": "Full name is required."
            }

        if not email:
            return {
                "success": False,
                "message": "Email is required."
            }

        existing_user = self.user_model.get_by_email(
            email
        )

        if existing_user and existing_user["id"] != user_id:
            return {
                "success": False,
                "message": "Email already in use."
            }

        if password:

            hashed_password = generate_password_hash(
                password
            )

        else:

            hashed_password = user["password"]

        # Atualiza os dados que pertencem à tabela USERS
        updated = self.user_model.update(
            user_id=user_id,
            full_name=full_name,
            email=email,
            password=hashed_password,
            profile_photo=profile_photo
        )

        if updated == 0:
            return {
                "success": False,
                "message": "Administrator was not updated."
            }

        # Atualiza o telefone que pertence à tabela ADMINISTRATORS
        self.administrator_model.update_phone(
            administrator_id,
            phone
        )

        return {
            "success": True,
            "message": "Administrator updated successfully.",
            "administrator_id": administrator_id,
            "user_id": user_id
        }



    def deactivate_administrator(
            self,
            admin_id,
            administrator_id
    ):

        administrator = self.administrator_model.get_by_id(
            administrator_id
        )

        if not administrator:
            return {
                "success": False,
                "message": "Administrator not found."
            }

        user_id = administrator["user_id"]

        user = self.administrator_model.get_user_by_id(
            user_id
        )

        if not user:
            return {
                "success": False,
                "message": "User not found."
            }

        if user["active"] == 0:
            return {
                "success": False,
                "message": "Administrator is already inactive."
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
                "message": "Administrator was not deactivated."
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
            "message": "Administrator deactivated successfully.",
            "administrator_id": administrator_id,
            "user_id": user_id
        }

    def activate_administrator(
            self,
            admin_id,
            administrator_id
    ):

        administrator = self.administrator_model.get_by_id(
            administrator_id
        )

        if not administrator:
            return {
                "success": False,
                "message": "Administrator not found."
            }

        user_id = administrator["user_id"]

        user = self.administrator_model.get_user_by_id(
            user_id
        )

        if not user:
            return {
                "success": False,
                "message": "User not found."
            }

        if user["active"] == 1:
            return {
                "success": False,
                "message": "Administrator is already active."
            }

        old_data = {
            "active": user["active"]
        }

        updated = self.user_model.activate(
            user_id
        )

        if updated == 0:
            return {
                "success": False,
                "message": "Administrator was not activated."
            }

        new_data = {
            "active": 1
        }

        self.audit_service.register(
            admin_id,
            "ACTIVATE",
            "users",
            user_id,
            old_data,
            new_data
        )

        return {
            "success": True,
            "message": "Administrator activated successfully.",
            "administrator_id": administrator_id,
            "user_id": user_id
        }