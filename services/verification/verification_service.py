from database.verification.verification_model import VerificationModel

from services.email.email_service import EmailService

import secrets
from datetime import datetime, timedelta


class VerificationService:

    def __init__(self):

        self.verification_model = VerificationModel()

        self.email_service = EmailService()


    def generate_code(self):

        return str(secrets.randbelow(900000) + 100000)


    def create_verification(
        self,
        email,
        phone
    ):

        email_code = self.generate_code()

        email_expires_at = (
            datetime.now() + timedelta(minutes=10)
        )


        verification_id = self.verification_model.create(

            email=email,

            phone=phone,

            email_code=email_code,

            phone_code=None,

            email_expires_at=email_expires_at,

            phone_expires_at=None

        )


        # ==========================================
        # ENVIO DO E-MAIL
        # ==========================================

        email_sent = self.email_service.send_email(

            recipient=email,

            subject="Verificação de e-mail - Precision Health Connect",

            message=f"""
            <h2>Olá!</h2>

            <p>
                Para continuar sua solicitação no
                <strong>Precision Health Connect</strong>,
                confirme seu endereço de e-mail.
            </p>

            <p>
                Seu código de verificação é:
            </p>

            <h1>{email_code}</h1>

            <p>
                Este código é válido por 10 minutos.
            </p>

            <p>
                Atenciosamente,<br>
                Equipe Precision Health Connect
            </p>
            """

        )


        # ==========================================
        # VERIFICAR ENVIO
        # ==========================================

        if not email_sent:

            self.verification_model.delete(
                verification_id
            )

            return {

                "success": False,

                "message": "Não foi possível enviar o código para este e-mail."

            }


        # ==========================================
        # SUCESSO
        # ==========================================

        return {

            "success": True,

            "message": "Código de verificação enviado.",

            "verification_id": verification_id,

            "email_sent": True

        }


    def verify_email(
        self,
        verification_id,
        code
    ):

        verification = self.verification_model.get_by_id(
            verification_id
        )


        if not verification:

            return {

                "success": False,

                "message": "Verificação não encontrada."

            }


        if verification["email_verified"] == 1:

            return {

                "success": True,

                "message": "E-mail já verificado."

            }


        if verification["email_code"] != code:

            return {

                "success": False,

                "message": "Código de e-mail inválido."

            }


        expires_at = datetime.fromisoformat(
            verification["email_expires_at"]
        )


        if datetime.now() > expires_at:

            return {

                "success": False,

                "message": "O código do e-mail expirou."

            }


        self.verification_model.mark_email_verified(
            verification_id
        )


        return {

            "success": True,

            "message": "E-mail verificado com sucesso."

        }


    def is_fully_verified(
        self,
        verification_id
    ):

        verification = self.verification_model.get_by_id(
            verification_id
        )


        if not verification:

            return False


        return verification["email_verified"] == 1

