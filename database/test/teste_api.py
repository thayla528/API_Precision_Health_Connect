import requests

url = "http://127.0.0.1:5001/api/messages"

dados = {
    "sender_id": 1,
    "receiver_id": 2,
    "message": "Olá, tudo bem?"
}

resposta = requests.post(url, json=dados)

print(resposta.status_code)
print(resposta.json())