
from database.invitations.invitation_model import InvitationModel
from database.users.user_model import UserModel

import secrets

from services.email.email_service import EmailService


class InvitationService:

    def __init__(self):

        self.invitation_model = InvitationModel()

        self.email_service = EmailService()


    # =====================================================
    # CRIAR SOLICITAÇÃO DE CONVITE
    # =====================================================

    def request_invitation(
        self,
        full_name,
        email,
        phone,
        birth_date,
        profile_type,
        interest_reason
    ):

        existing_invitation = (
            self.invitation_model.get_by_email(email)
        )


        if existing_invitation:

            return {

                "success": False,

                "message":
                    "An invitation request already exists for this email."

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

            "message":
                "Invitation request created successfully.",

            "invitation_id":
                invitation_id

        }


    # =====================================================
    # APROVAR SOLICITAÇÃO
    # =====================================================

    def approve_invitation(
        self,
        invitation_id,
        administrator_id
    ):

        invitation = (
            self.invitation_model.get_by_id(
                invitation_id
            )
        )


        if not invitation:

            return {

                "success": False,

                "message":
                    "Invitation not found."

            }


        if invitation["status"] != "pending":

            return {

                "success": False,

                "message":
                    "Only pending invitations can be approved."

            }


        # =================================================
        # GERAR CÓDIGO DO CONVITE
        # =================================================

        invitation_code = secrets.token_hex(4)


        # =================================================
        # SALVAR APROVAÇÃO NO BANCO
        # =================================================

        self.invitation_model.approve(

            invitation_id,

            invitation_code,

            administrator_id

        )


        # =================================================
        # ENVIAR E-MAIL DE APROVAÇÃO
        # =================================================

        email_sent = self.email_service.send_email(

            recipient=invitation["email"],

            subject="Cadastro aprovado - Precision Health Connect",

            message=f"""

            <h2>Olá, {invitation['full_name']}!</h2>

            <p>
                Seu cadastro no
                <strong>Precision Health Connect</strong>
                foi aprovado.
            </p>

            <p>
                Agora você já pode finalizar seu cadastro
                utilizando o código abaixo:
            </p>

            <p>
                <strong>Código do convite:</strong>
            </p>

            <h1>
                {invitation_code}
            </h1>

            <p>
                Utilize este código na página de finalização
                do cadastro.
            </p>

            <p>
                Atenciosamente,<br>
                Equipe Precision Health Connect.
            </p>

            """

        )


        # =================================================
        # VERIFICAR ENVIO DO E-MAIL
        # =================================================

        if not email_sent:

            return {

                "success": False,

                "message":
                    "Convite aprovado, mas não foi possível enviar o e-mail.",

                "invitation_code":
                    invitation_code

            }


        # =================================================
        # SUCESSO
        # =================================================

        return {

            "success": True,

            "message":
                "Invitation approved successfully. Approval email sent.",

            "invitation_code":
                invitation_code,

            "email_sent":
                True

        }


    # =====================================================
    # LISTAR TODAS AS SOLICITAÇÕES
    # =====================================================

    def get_all_invitations(self):

        invitations = self.invitation_model.get_all()


        invitation_list = []


        for invitation in invitations:

            invitation_list.append(
                dict(invitation)
            )


        return invitation_list


    # =====================================================
    # FINALIZAR CADASTRO PELO CONVITE
    # =====================================================

    def register_with_invitation(
        self,
        invitation_code,
        password
    ):

        # =================================================
        # BUSCAR CONVITE
        # =================================================

        invitation = (
            self.invitation_model.get_by_code(
                invitation_code
            )
        )


        if not invitation:

            return {

                "success": False,

                "message":
                    "Código de convite inválido."

            }


        # =================================================
        # VERIFICAR STATUS
        # =================================================

        if invitation["status"] != "approved":

            return {

                "success": False,

                "message":
                    "Convite ainda não aprovado."

            }


        # =================================================
        # VERIFICAR SE JÁ FOI UTILIZADO
        # =================================================

        if invitation["used"] == 1:

            return {

                "success": False,

                "message":
                    "Convite já utilizado."

            }


        # =================================================
        # CRIAR USUÁRIO
        # =================================================

        try:

            user_id = UserModel.create(
                invitation_id=invitation["id"],
                full_name=invitation["full_name"],
                email=invitation["email"],
                password=password,
                profile_type=invitation["profile_type"],
                profile_photo=None,
                phone=invitation["phone"]
            )

        except Exception as e:

            print(
                "Erro ao criar usuário:",
                e
            )

            return {

                "success": False,

                "message":
                    "Não foi possível criar a conta."

            }


        # =================================================
        # MARCAR CONVITE COMO UTILIZADO
        # =================================================

        self.invitation_model.mark_as_used(

            invitation["id"]

        )


        # =================================================
        # ENVIAR E-MAIL DE CONTA CRIADA
        # =================================================

        email_sent = self.email_service.send_email(

            recipient=invitation["email"],

            subject="Conta criada com sucesso - Precision Health Connect",

            message=f"""

            <h2>Olá, {invitation['full_name']}!</h2>

            <p>
                Sua conta no
                <strong>Precision Health Connect</strong>
                foi criada com sucesso.
            </p>

            <p>
                Seu cadastro foi finalizado e sua conta
                já está pronta para utilização.
            </p>

            <p>
                Você já pode acessar a plataforma utilizando
                seu e-mail e sua senha cadastrada.
            </p>

            <p>
                <strong>ID da sua conta:</strong>
                {user_id}
            </p>

            <p>
                Atenciosamente,<br>
                Equipe Precision Health Connect.
            </p>

            """

        )


        # =================================================
        # CONTA CRIADA
        # =================================================

        return {

            "success": True,

            "message":
                "Cadastro finalizado com sucesso.",

            "user_id":
                user_id,

            "email_sent":
                email_sent

        }


    # =====================================================
    # REJEITAR SOLICITAÇÃO
    # =====================================================

    def reject_invitation(
        self,
        invitation_id,
        administrator_id
    ):

        invitation = (
            self.invitation_model.get_by_id(
                invitation_id
            )
        )


        if not invitation:

            return {

                "success": False,

                "message":
                    "Invitation not found."

            }


        if invitation["status"] != "pending":

            return {

                "success": False,

                "message":
                    "Only pending invitations can be rejected."

            }


        self.invitation_model.reject(

            invitation_id,

            administrator_id

        )


        return {

            "success": True,

            "message":
                "Invitation rejected successfully."

        }


    # =====================================================
    # VALIDAR CÓDIGO DO CONVITE
    # =====================================================

    def validate_invitation_code(
        self,
        invitation_code
    ):

        invitation = (
            self.invitation_model.get_by_code(
                invitation_code
            )
        )


        if not invitation:

            return {

                "success": False,

                "message":
                    "Invalid invitation code."

            }


        if invitation["status"] != "approved":

            return {

                "success": False,

                "message":
                    "Invitation is not approved."

            }


        return {

            "success": True,

            "message":
                "Invitation validated successfully.",

            "invitation":
                invitation

        }

