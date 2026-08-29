
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

        # =====================================================
        # CARREGAR CONFIGURAÇÕES DO E-MAIL
        # =====================================================

        email_address = os.getenv(
            "EMAIL_ADDRESS"
        )

        email_password = os.getenv(
            "EMAIL_PASSWORD"
        )

        smtp_server = os.getenv(
            "SMTP_SERVER"
        )

        smtp_port = os.getenv(
            "SMTP_PORT"
        )


        # =====================================================
        # VERIFICAR CONFIGURAÇÕES
        # =====================================================

        print("")
        print("========================================")
        print("CONFIGURAÇÃO DO E-MAIL")
        print("========================================")

        print(
            "EMAIL_ADDRESS:",
            email_address
        )

        print(
            "EMAIL_PASSWORD:",
            "CONFIGURADA"
            if email_password
            else "NÃO CONFIGURADA"
        )

        print(
            "SMTP_SERVER:",
            smtp_server
        )

        print(
            "SMTP_PORT:",
            smtp_port
        )

        print(
            "DESTINATÁRIO:",
            recipient
        )

        print("========================================")
        print("")


        # =====================================================
        # VALIDAR CONFIGURAÇÕES
        # =====================================================

        if not email_address:

            print(
                "ERRO: EMAIL_ADDRESS não foi configurado."
            )

            return False


        if not email_password:

            print(
                "ERRO: EMAIL_PASSWORD não foi configurado."
            )

            return False


        if not smtp_server:

            print(
                "ERRO: SMTP_SERVER não foi configurado."
            )

            return False


        if not smtp_port:

            print(
                "ERRO: SMTP_PORT não foi configurado."
            )

            return False


        # =====================================================
        # CONVERTER PORTA
        # =====================================================

        try:

            smtp_port = int(
                smtp_port
            )

        except ValueError:

            print(
                "ERRO: SMTP_PORT precisa ser um número."
            )

            return False


        # =====================================================
        # CRIAR E-MAIL
        # =====================================================

        try:

            email = MIMEMultipart(
                "alternative"
            )


            # =================================================
            # REMETENTE
            # =================================================

            email["From"] = formataddr(
                (
                    str(
                        Header(
                            "Precision Health Connect",
                            "utf-8"
                        )
                    ),

                    email_address
                )
            )


            # =================================================
            # DESTINATÁRIO
            # =================================================

            email["To"] = recipient


            # =================================================
            # ASSUNTO
            # =================================================

            email["Subject"] = subject


            # =================================================
            # REPLY-TO
            # =================================================

            email["Reply-To"] = email_address


            # =================================================
            # HTML DO E-MAIL
            # =================================================

            html_content = f"""
            <!DOCTYPE html>

            <html lang="pt-BR">

            <head>

                <meta charset="UTF-8">

                <meta
                    name="viewport"
                    content="width=device-width, initial-scale=1.0"
                >

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

                                            <strong
                                                style="
                                                    color: #68747c;
                                                "
                                            >
                                                Precision Health Connect
                                            </strong>.

                                        </div>


                                        <div style="
                                            margin-top: 8px;
                                            font-size: 11px;
                                            color: #b0b7bc;
                                        ">

                                            Por favor, não responda
                                            automaticamente a esta mensagem.

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


            # =================================================
            # ANEXAR HTML
            # =================================================

            html = MIMEText(
                html_content,
                "html",
                "utf-8"
            )


            email.attach(
                html
            )


            # =================================================
            # CONECTAR AO SERVIDOR SMTP
            # =================================================

            print("")
            print("Conectando ao servidor SMTP...")
            print(
                "Servidor:",
                smtp_server
            )
            print(
                "Porta:",
                smtp_port
            )


            server = smtplib.SMTP(
                smtp_server,
                smtp_port,
                timeout=30
            )


            print(
                "Conexão SMTP estabelecida."
            )


            # =================================================
            # ATIVAR TLS
            # =================================================

            print(
                "Iniciando TLS..."
            )

            server.starttls()

            print(
                "TLS iniciado com sucesso."
            )


            # =================================================
            # LOGIN
            # =================================================

            print(
                "Realizando login SMTP..."
            )

            server.login(
                email_address,
                email_password
            )

            print(
                "Login SMTP realizado com sucesso."
            )


            # =================================================
            # ENVIAR
            # =================================================

            print("")
            print(
                "Enviando e-mail para:",
                recipient
            )

            server.send_message(
                email
            )


            # =================================================
            # ENCERRAR CONEXÃO
            # =================================================

            server.quit()


            print("")
            print(
                "========================================"
            )

            print(
                "E-MAIL ENVIADO COM SUCESSO!"
            )

            print(
                "========================================"
            )

            print("")


            return True


        # =====================================================
        # ERRO
        # =====================================================

        except smtplib.SMTPAuthenticationError as e:

            print("")
            print(
                "========================================"
            )

            print(
                "ERRO DE AUTENTICAÇÃO SMTP"
            )

            print(
                "========================================"
            )

            print(
                "Verifique o e-mail e a senha SMTP."
            )

            print(
                "Detalhes:",
                e
            )

            print("")

            return False


        except smtplib.SMTPConnectError as e:

            print("")
            print(
                "========================================"
            )

            print(
                "ERRO AO CONECTAR AO SERVIDOR SMTP"
            )

            print(
                "========================================"
            )

            print(
                "Servidor:",
                smtp_server
            )

            print(
                "Porta:",
                smtp_port
            )

            print(
                "Detalhes:",
                e
            )

            print("")

            return False


        except smtplib.SMTPException as e:

            print("")
            print(
                "========================================"
            )

            print(
                "ERRO SMTP"
            )

            print(
                "========================================"
            )

            print(
                "Detalhes:",
                e
            )

            print("")

            return False


        except Exception as e:

            print("")
            print(
                "========================================"
            )

            print(
                "ERRO AO ENVIAR E-MAIL"
            )

            print(
                "========================================"
            )

            print(
                "Tipo do erro:",
                type(e).__name__
            )

            print(
                "Detalhes:",
                e
            )

            print("")

            return False
