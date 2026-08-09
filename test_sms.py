from services.sms.sms_service import SMSService

sms_service = SMSService()


result = sms_service.send_sms(
    recipient="11999999999",
    message="Seu código de verificação é 123456."
)


print("Resultado:", result)