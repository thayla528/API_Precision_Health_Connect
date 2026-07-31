import os

from dotenv import load_dotenv
from flask_jwt_extended import JWTManager


load_dotenv()


def configure_jwt(app):

    app.config["JWT_SECRET_KEY"] = os.getenv(
        "JWT_SECRET_KEY"
    )

    jwt = JWTManager(app)

    return jwt