import os
import smtplib

from dotenv import load_dotenv

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
from email.utils import formataddr


load_dotenv()


class EmailService:

    def send_email(
            self,
            recipient,
            subject,
            message
    ):

        email_address = os.getenv("EMAIL_ADDRESS")
        email_password = os.getenv("EMAIL_PASSWORD")
        smtp_server = os.getenv("SMTP_SERVER")
        smtp_port = int(os.getenv("SMTP_PORT"))


        try:

            email = MIMEMultipart("alternative")


            email["From"] = formataddr(
                (
                    str(Header("Precision Health Connect", "utf-8")),
                    email_address
                )
            )

            email["To"] = recipient
            email["Subject"] = subject
            email["Reply-To"] = email_address


            html_content = message


            html = MIMEText(
                html_content,
                "html",
                "utf-8"
            )


            email.attach(html)


            print("Enviando e-mail para:", recipient)


            server = smtplib.SMTP(
                smtp_server,
                smtp_port
            )

            server.starttls()


            server.login(
                email_address,
                email_password
            )


            server.send_message(email)


            server.quit()


            print("E-mail enviado com sucesso!")

            return True


        except Exception as e:

            print("Erro ao enviar e-mail:", e)

            return False