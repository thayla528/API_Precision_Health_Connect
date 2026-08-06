from flask import Flask


from routes.users.user_api import user_api_bp
from routes.invitations.invitation_api import invitation_api_bp
from routes.users.auth_api import auth_api_bp
from routes.patients.patient_api import patient_api_bp
from routes.messages.message_api import message_bp
from routes.patients.patient_professional_api import patient_professional_bp
from routes.professionals.professional_profile_api import professional_profile_bp
from routes.appointments.appointment_api import appointment_bp


from routes.notifications.notifications_api import notification_bp

from routes.clinical_records.clinical_record_api import clinical_record_bp

from routes.medical_documents.medical_documents_api import medical_document_bp

from security.jwt_config import configure_jwt

from routes.users.token_api import token_bp

from routes.users.logout_api import logout_bp

from security.rate_limit import limiter

from flask import jsonify

app = Flask(__name__)

limiter.init_app(app)

configure_jwt(app)

from config import (
    UPLOAD_FOLDER,
    MAX_CONTENT_LENGTH
)

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

app.config["MAX_CONTENT_LENGTH"] = MAX_CONTENT_LENGTH



# ---------------- BLUEPRINTS ----------------

app.register_blueprint(user_api_bp)

app.register_blueprint(invitation_api_bp)

app.register_blueprint(auth_api_bp)

app.register_blueprint(patient_api_bp)

app.register_blueprint(message_bp, url_prefix="/api")

app.register_blueprint(professional_profile_bp)

app.register_blueprint(patient_professional_bp)

app.register_blueprint(appointment_bp)

app.register_blueprint(notification_bp)

app.register_blueprint(clinical_record_bp)

app.register_blueprint(medical_document_bp)

app.register_blueprint(token_bp)

app.register_blueprint(logout_bp)

print(app.url_map)

# ---------------- RUN ----------------

@app.errorhandler(429)
def ratelimit_handler(e):

    return jsonify({

        "success": False,

        "message": "Too many requests. Please try again later."

    }), 429

if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5001,
        debug=True
    )