
import secrets
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash
from database.users.user_model import UserModel
from database.users.password_reset_model import PasswordResetModel

from services.email.email_service import EmailService


class PasswordResetService:

    def __init__(self):

        self.user_model = UserModel()

        self.password_reset_model = PasswordResetModel()

        self.email_service = EmailService()


    # =====================================================
    # SOLICITAR RECUPERAÇÃO DE SENHA
    # =====================================================

    def request_password_reset(
        self,
        email
    ):

        print("")
        print("==============================================")
        print("INÍCIO DA RECUPERAÇÃO DE SENHA")
        print("==============================================")

        print(
            "E-mail recebido:",
            email
        )


        # -------------------------------------------------
        # BUSCAR USUÁRIO
        # -------------------------------------------------

        print("")
        print("1. Buscando usuário pelo e-mail...")

        user = self.user_model.get_by_email(
            email
        )


        if user:

            print(
                "Usuário encontrado."
            )

            print(
                "ID do usuário:",
                user["id"]
            )

            print(
                "E-mail do usuário:",
                user["email"]
            )

        else:

            print(
                "USUÁRIO NÃO ENCONTRADO."
            )


        # -------------------------------------------------
        # RESPOSTA GENÉRICA
        # -------------------------------------------------

        generic_response = {

            "success": True,

            "message":
                "Se houver uma conta associada a este e-mail, "
                "enviamos as instruções para recuperação da senha."

        }


        if not user:

            print("")
            print(
                "Encerrando processo porque o usuário não existe."
            )

            print("==============================================")
            print("FIM DA RECUPERAÇÃO")
            print("==============================================")
            print("")

            return generic_response


        # -------------------------------------------------
        # GERAR CÓDIGO DE 6 DÍGITOS
        # -------------------------------------------------

        print("")
        print("2. Gerando código de recuperação...")

        reset_code = str(
            secrets.randbelow(1000000)
        ).zfill(6)

        print(
            "Código gerado com sucesso."
        )

        print(
            "Código:",
            reset_code
        )

        print(
            "Tamanho do código:",
            len(reset_code)
        )


        # -------------------------------------------------
        # DEFINIR EXPIRAÇÃO
        # -------------------------------------------------

        print("")
        print("3. Definindo expiração do código...")

        expires_at = (
            datetime.utcnow()
            + timedelta(minutes=10)
        )

        print(
            "Código válido até:",
            expires_at
        )


        # -------------------------------------------------
        # SALVAR CÓDIGO
        # -------------------------------------------------

        print("")
        print("4. Salvando código no banco de dados...")

        try:

            self.password_reset_model.create(

                user_id=user["id"],

                email=user["email"],

                reset_code=reset_code,

                expires_at=expires_at

            )

            print(
                "Código salvo no banco com sucesso."
            )

        except Exception as e:

            print("")
            print(
                "ERRO AO SALVAR CÓDIGO NO BANCO!"
            )

            print(
                "Tipo:",
                type(e).__name__
            )

            print(
                "Erro:",
                e
            )

            print("==============================================")
            print("")

            return {

                "success": False,

                "message":
                    "Erro ao criar recuperação de senha."

            }


        # -------------------------------------------------
        # ENVIAR CÓDIGO POR E-MAIL
        # -------------------------------------------------

        print("")
        print("5. Chamando EmailService...")

        print(
            "Destinatário:",
            user["email"]
        )


        try:

            email_sent = self.email_service.send_email(

                recipient=user["email"],

                subject=(
                    "Código de recuperação de senha - "
                    "Precision Health Connect"
                ),

                message=f"""

                <h2>Olá, {user['full_name']}!</h2>

                <p>
                    Recebemos uma solicitação para redefinir
                    a senha da sua conta no
                    <strong>Precision Health Connect</strong>.
                </p>

                <p>
                    Seu código de recuperação é:
                </p>

                <p style="
                    text-align: center;
                    margin: 30px 0;
                ">

                    <span style="
                        display: inline-block;
                        padding: 18px 30px;
                        background-color: #f1f5f9;
                        color: #1e293b;
                        border-radius: 10px;
                        font-size: 32px;
                        font-weight: bold;
                        letter-spacing: 8px;
                    ">
                        {reset_code}
                    </span>

                </p>

                <p>
                    Digite este código na tela de recuperação
                    de senha para continuar.
                </p>

                <p>
                    Este código ficará disponível por
                    <strong>10 minutos</strong>.
                </p>

                <p>
                    Se você não solicitou a recuperação da senha,
                    ignore este e-mail.
                </p>

                <p>
                    Atenciosamente,<br>
                    Equipe Precision Health Connect.
                </p>

                """

            )


            print("")
            print(
                "Resultado retornado pelo EmailService:",
                email_sent
            )


        except Exception as e:

            print("")
            print(
                "ERRO AO CHAMAR EMAILSERVICE!"
            )

            print(
                "Tipo:",
                type(e).__name__
            )

            print(
                "Erro:",
                e
            )

            print("==============================================")
            print("")

            return {

                "success": False,

                "message":
                    "Erro ao tentar enviar o e-mail."

            }


        # -------------------------------------------------
        # VERIFICAR ENVIO
        # -------------------------------------------------

        print("")
        print("6. Verificando resultado do envio...")


        if not email_sent:

            print("")
            print(
                "O EMAILSERVICE RETORNOU FALSE."
            )

            print(
                "O e-mail NÃO foi enviado."
            )

            print("==============================================")
            print("")


            return {

                "success": False,

                "message":
                    "Não foi possível enviar o e-mail de recuperação."

            }


        # -------------------------------------------------
        # SUCESSO
        # -------------------------------------------------

        print("")
        print(
            "E-MAIL PROCESSADO COM SUCESSO!"
        )

        print(
            "Código de recuperação enviado."
        )

        print("==============================================")
        print("FIM DA RECUPERAÇÃO")
        print("==============================================")
        print("")


        return generic_response


    # =====================================================
    # VALIDAR CÓDIGO DE RECUPERAÇÃO
    # =====================================================

    def validate_reset_token(
        self,
        reset_code
    ):

        print("")
        print("==============================================")
        print("VALIDANDO CÓDIGO DE RECUPERAÇÃO")
        print("==============================================")

        print(
            "Código recebido:",
            reset_code
        )


        # -------------------------------------------------
        # BUSCAR CÓDIGO
        # -------------------------------------------------

        print("")
        print("1. Buscando código no banco...")

        reset = (
            self.password_reset_model
            .get_by_code(reset_code)
        )


        if not reset:

            print(
                "Código não encontrado."
            )

            print("==============================================")
            print("CÓDIGO INVÁLIDO")
            print("==============================================")
            print("")

            return {

                "success": False,

                "message":
                    "Código de recuperação inválido."

            }


        print(
            "Código encontrado."
        )


        # -------------------------------------------------
        # VERIFICAR SE JÁ FOI UTILIZADO
        # -------------------------------------------------

        print("")
        print("2. Verificando se o código já foi utilizado...")


        if reset["used"] == 1:

            print(
                "Código já utilizado."
            )

            return {

                "success": False,

                "message":
                    "Este código de recuperação já foi utilizado."

            }


        print(
            "Código ainda não foi utilizado."
        )


        # -------------------------------------------------
        # VERIFICAR EXPIRAÇÃO
        # -------------------------------------------------

        print("")
        print("3. Verificando expiração...")


        expires_at = datetime.fromisoformat(
            reset["expires_at"]
        )


        if datetime.utcnow() > expires_at:

            print(
                "Código expirado."
            )

            return {

                "success": False,

                "message":
                    "Este código de recuperação expirou."

            }


        print(
            "Código ainda está válido."
        )


        print("")
        print("==============================================")
        print("CÓDIGO VÁLIDO")
        print("==============================================")
        print("")


        return {

            "success": True,

            "message":
                "Código válido.",

            "reset":
                reset

        }


    # =====================================================
    # REDEFINIR SENHA
    # =====================================================

    def reset_password(
        self,
        reset_code,
        new_password,
        confirm_password
    ):

        print("")
        print("==============================================")
        print("REDEFININDO SENHA")
        print("==============================================")

        print(
            "Código recebido:",
            reset_code
        )


        # -------------------------------------------------
        # VALIDAR SENHAS
        # -------------------------------------------------

        print("")
        print("1. Validando nova senha...")


        if not new_password:

            print(
                "Nova senha não informada."
            )

            return {

                "success": False,

                "message":
                    "A nova senha é obrigatória."

            }


        if not confirm_password:

            print(
                "Confirmação da senha não informada."
            )

            return {

                "success": False,

                "message":
                    "A confirmação da senha é obrigatória."

            }


        if new_password != confirm_password:

            print(
                "As senhas não coincidem."
            )

            return {

                "success": False,

                "message":
                    "As senhas não coincidem."

            }


        print(
            "Nova senha válida."
        )


        # -------------------------------------------------
        # VALIDAR CÓDIGO
        # -------------------------------------------------

        print("")
        print("2. Validando código de recuperação...")


        result = self.validate_reset_token(
            reset_code
        )


        if not result["success"]:

            print(
                "Código inválido."
            )

            return result


        reset = result["reset"]


        print(
            "Código válido."
        )


        # -------------------------------------------------
        # GERAR HASH DA NOVA SENHA
        # -------------------------------------------------

        print("")
        print("3. Gerando hash da nova senha...")


        hashed_password = generate_password_hash(
            new_password
        )


        # -------------------------------------------------
        # CONFIRMAR QUE O HASH FOI GERADO
        # -------------------------------------------------

        if not hashed_password:

            print(
                "ERRO: O HASH NÃO FOI GERADO."
            )

            return {

                "success": False,

                "message":
                    "Não foi possível proteger a nova senha."

            }


        print(
            "Hash da senha gerado com sucesso."
        )

        print(
            "Algoritmo do hash:",
            hashed_password.split(":")[0]
        )


        # -------------------------------------------------
        # ATUALIZAR SENHA DO USUÁRIO
        # -------------------------------------------------

        print("")
        print("4. Atualizando senha do usuário...")


        try:

            updated = self.user_model.update_password(

                reset["user_id"],

                hashed_password

            )


        except Exception as e:

            print("")
            print(
                "ERRO AO ATUALIZAR SENHA!"
            )

            print(
                "Tipo:",
                type(e).__name__
            )

            print(
                "Erro:",
                e
            )

            return {

                "success": False,

                "message":
                    "Não foi possível atualizar a senha."

            }


        if updated == 0:

            print(
                "Nenhuma senha foi atualizada."
            )

            return {

                "success": False,

                "message":
                    "Não foi possível atualizar a senha."

            }


        print(
            "Senha atualizada com sucesso."
        )


        # -------------------------------------------------
        # INVALIDAR CÓDIGO
        # -------------------------------------------------

        print("")
        print("5. Marcando código como utilizado...")


        try:

            marked = self.password_reset_model.mark_as_used(

                reset["id"]

            )


            if marked == 0:

                print(
                    "AVISO: O código não foi marcado como utilizado."
                )

            else:

                print(
                    "Código marcado como utilizado."
                )


        except Exception as e:

            print(
                "ERRO AO INVALIDAR CÓDIGO:",
                e
            )


        # -------------------------------------------------
        # ENVIAR E-MAIL DE CONFIRMAÇÃO
        # -------------------------------------------------

        print("")
        print("6. Enviando e-mail de confirmação...")


        try:

            email_sent = self.email_service.send_email(

                recipient=reset["email"],

                subject=(
                    "Senha redefinida com sucesso - "
                    "Precision Health Connect"
                ),

                message="""

                <h2>Senha redefinida com sucesso</h2>

                <p>
                    Sua senha do
                    <strong>Precision Health Connect</strong>
                    foi redefinida com sucesso.
                </p>

                <p>
                    A partir de agora, você pode acessar sua conta
                    utilizando sua nova senha.
                </p>

                <p>
                    Se você não realizou esta alteração,
                    entre em contato com a equipe responsável
                    pela plataforma imediatamente.
                </p>

                <p>
                    Atenciosamente,<br>
                    Equipe Precision Health Connect.
                </p>

                """

            )


            print(
                "Resultado do envio:",
                email_sent
            )


        except Exception as e:

            print("")
            print(
                "ERRO AO ENVIAR E-MAIL DE CONFIRMAÇÃO!"
            )

            print(
                "Tipo:",
                type(e).__name__
            )

            print(
                "Erro:",
                e
            )

            email_sent = False


        # -------------------------------------------------
        # SUCESSO
        # -------------------------------------------------

        print("")
        print("==============================================")
        print("SENHA REDEFINIDA COM SUCESSO")
        print("==============================================")
        print("")


        return {

            "success": True,

            "message":
                "Senha redefinida com sucesso."

        }

