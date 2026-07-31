import os

from cryptography.fernet import Fernet
from dotenv import load_dotenv


load_dotenv()


KEY = os.getenv("FERNET_KEY").encode()


cipher = Fernet(KEY)


def encrypt_message(message):

    encrypted = cipher.encrypt(
        message.encode()
    )

    return encrypted.decode()


def decrypt_message(encrypted_message):

    decrypted = cipher.decrypt(
        encrypted_message.encode()
    )

    return decrypted.decode()