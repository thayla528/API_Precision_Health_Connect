from flask import Flask



from routes.user_api import user_api_bp
from routes.invitation_api import invitation_api_bp
from routes.auth_api import auth_api_bp
from routes.patient_api import patient_api_bp
from routes.message_api import message_bp
from routes.patient_professional_api import patient_professional_bp
from security.jwt_config import configure_jwt


app = Flask(__name__)

configure_jwt(app)

# ---------------- BLUEPRINTS ----------------



app.register_blueprint(user_api_bp)

app.register_blueprint(invitation_api_bp)

app.register_blueprint(auth_api_bp)

app.register_blueprint(patient_api_bp)

app.register_blueprint(patient_professional_bp)

app.register_blueprint(message_bp,url_prefix="/api")


# ---------------- RUN ----------------

if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5001,
        debug=True
    )