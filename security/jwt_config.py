import os

from datetime import timedelta

from dotenv import load_dotenv

from flask_jwt_extended import (
    JWTManager,
    get_jwt
)

from database.security.revoked_token_model import RevokedTokenModel


load_dotenv()



def configure_jwt(app):


    app.config["JWT_SECRET_KEY"] = os.getenv(
        "JWT_SECRET_KEY"
    )


    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(
        minutes=15
    )


    app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(
        days=30
    )


    jwt = JWTManager(app)



    @jwt.token_in_blocklist_loader
    def check_if_token_revoked(
            jwt_header,
            jwt_payload
    ):

        jti = jwt_payload["jti"]


        return RevokedTokenModel.is_revoked(
            jti
        )



    return jwt