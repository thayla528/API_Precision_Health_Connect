
class SMSService:

    def send_sms(
        self,
        recipient,
        message
    ):

        try:

            print()
            print("========================================")
            print("           SMS DE TESTE")
            print("========================================")
            print("Enviando SMS para:", recipient)
            print("Mensagem:")
            print(message)
            print("========================================")
            print()

            return True

        except Exception as e:

            print("Erro ao enviar SMS:", e)

            return False

