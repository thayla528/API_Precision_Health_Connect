import os
import smtplib
from email.header import Header
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formataddr


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

            # ---------------------------------------------------------
            # FRONTEND DO E-MAIL
            # O conteúdo original de "message" é mantido.
            # Apenas adicionamos uma estrutura visual ao redor dele.
            # ---------------------------------------------------------

            html_content = f"""
            <!DOCTYPE html>
            <html lang="pt-BR">
    
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
    
                <title>{subject}</title>
            </head>
    
            <body style="
                margin: 0;
                padding: 0;
                background-color: #f5f7f9;
                font-family: Arial, Helvetica, sans-serif;
                color: #263238;
            ">
    
                <table
                    width="100%"
                    cellpadding="0"
                    cellspacing="0"
                    border="0"
                    style="
                        background-color: #f5f7f9;
                        padding: 40px 15px;
                    "
                >
    
                    <tr>
                        <td align="center">
    
                            <!-- CONTAINER PRINCIPAL -->
                            <table
                                width="100%"
                                cellpadding="0"
                                cellspacing="0"
                                border="0"
                                style="
                                    max-width: 600px;
                                    background-color: #ffffff;
                                    border-radius: 14px;
                                    overflow: hidden;
                                    border: 1px solid #e8ecef;
                                "
                            >
    
                                <!-- CABEÇALHO -->
                                <tr>
                                    <td
                                        style="
                                            padding: 32px 35px;
                                            text-align: center;
                                            border-bottom: 1px solid #eef1f3;
                                        "
                                    >
    
                                        <div style="
                                            font-size: 22px;
                                            font-weight: bold;
                                            letter-spacing: 0.3px;
                                            color: #1f2933;
                                        ">
                                            Precision Health Connect
                                        </div>
    
                                        <div style="
                                            margin-top: 7px;
                                            font-size: 12px;
                                            color: #8a959e;
                                            letter-spacing: 1px;
                                            text-transform: uppercase;
                                        ">
                                            Saúde • Tecnologia • Conexão
                                        </div>
    
                                    </td>
                                </tr>
    
    
                                <!-- CONTEÚDO -->
                                <tr>
                                    <td
                                        style="
                                            padding: 38px 40px;
                                            font-size: 15px;
                                            line-height: 1.7;
                                            color: #39444d;
                                        "
                                    >
    
                                        {message}
    
                                    </td>
                                </tr>
    
    
                                <!-- RODAPÉ -->
                                <tr>
                                    <td
                                        style="
                                            padding: 24px 35px;
                                            background-color: #fafbfc;
                                            border-top: 1px solid #eef1f3;
                                            text-align: center;
                                        "
                                    >
    
                                        <div style="
                                            font-size: 12px;
                                            line-height: 1.6;
                                            color: #9aa4ab;
                                        ">
                                            Este e-mail foi enviado pelo
                                            <strong style="color: #68747c;">
                                                Precision Health Connect
                                            </strong>.
                                        </div>
    
                                        <div style="
                                            margin-top: 8px;
                                            font-size: 11px;
                                            color: #b0b7bc;
                                        ">
                                            Por favor, não responda automaticamente a esta mensagem.
                                        </div>
    
                                    </td>
                                </tr>
    
                            </table>
    
                        </td>
                    </tr>
    
                </table>
    
            </body>
    
            </html>
            """

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
