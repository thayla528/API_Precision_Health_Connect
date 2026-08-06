from database.invitations.invitation_model import InvitationModel

import secrets

from services.email.email_service import EmailService

class InvitationService:

    def __init__(self):
        self.invitation_model = InvitationModel()

        self.email_service = EmailService()


    def request_invitation(
        self,
        full_name,
        email,
        phone,
        birth_date,
        profile_type,
        interest_reason
    ):

        existing_invitation = self.invitation_model.get_by_email(email)

        if existing_invitation:
            return {
                "success": False,
                "message": "An invitation request already exists for this email."
            }


        invitation_id = self.invitation_model.create(
            full_name,
            email,
            phone,
            birth_date,
            profile_type,
            interest_reason
        )


        return {
            "success": True,
            "message": "Invitation request created successfully.",
            "invitation_id": invitation_id
        }

    def approve_invitation(
            self,
            invitation_id,
            administrator_id
    ):

        invitation = self.invitation_model.get_by_id(invitation_id)

        if not invitation:
            return {
                "success": False,
                "message": "Invitation not found."
            }

        if invitation["status"] != "pending":
            return {
                "success": False,
                "message": "Only pending invitations can be approved."
            }

        invitation_code = secrets.token_hex(4)

        self.invitation_model.approve(
            invitation_id,
            invitation_code,
            administrator_id
        )

        self.email_service.send_email(

            recipient=invitation["email"],

            subject="Cadastro aprovado",

            message=f"""
        Olá, {invitation['full_name']}!

        Seu cadastro no Precision Health Connect foi aprovado.

        Agora você já pode finalizar seu cadastro.

        Código do convite:

        {invitation_code}

        Atenciosamente,

        Equipe Precision Health Connect.
        """

        )

        return {
            "success": True,
            "message": "Invitation approved successfully.",
            "invitation_code": invitation_code
        }

    def get_all_invitations(self):

        invitations = self.invitation_model.get_all()

        invitation_list = []

        for invitation in invitations:
            invitation_list.append(dict(invitation))

        return invitation_list

    def register_with_invitation(
            self,
            invitation_code,
            password
    ):

        invitation = self.invitation_model.get_by_code(
            invitation_code
        )

        if not invitation:
            return {
                "success": False,
                "message": "Código de convite inválido."
            }

        if invitation["status"] != "approved":
            return {
                "success": False,
                "message": "Convite ainda não aprovado."
            }

        if invitation["used"] == 1:
            return {
                "success": False,
                "message": "Convite já utilizado."
            }

        # AQUI VAI CRIAR O USUÁRIO
        # usando os dados da invitation

        return {

            "success": True,

            "message": "Cadastro finalizado."

        }

    def reject_invitation(
            self,
            invitation_id,
            administrator_id
    ):

        invitation = self.invitation_model.get_by_id(invitation_id)

        if not invitation:
            return {
                "success": False,
                "message": "Invitation not found."
            }

        if invitation["status"] != "pending":
            return {
                "success": False,
                "message": "Only pending invitations can be rejected."
            }

        self.invitation_model.reject(
            invitation_id,
            administrator_id
        )

        return {
            "success": True,
            "message": "Invitation rejected successfully."
        }

    def validate_invitation_code(
            self,
            invitation_code
    ):

        invitation = self.invitation_model.get_by_code(invitation_code)

        if not invitation:
            return {
                "success": False,
                "message": "Invalid invitation code."
            }

        if invitation["status"] != "approved":
            return {
                "success": False,
                "message": "Invitation is not approved."
            }

        return {
            "success": True,
            "message": "Invitation validated successfully.",
            "invitation": invitation
        }





