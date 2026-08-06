from flask import Blueprint, request, jsonify

from flask_jwt_extended import (
    jwt_required,
    get_jwt_identity
)

import os

import uuid

from werkzeug.utils import secure_filename

from security.permissions import role_required

from services.medical_documents.medical_documents_service import MedicalDocumentService

from services.security_service.access_control_service import AccessControlService



medical_document_bp = Blueprint(
    "medical_document",
    __name__,
    url_prefix="/medical-documents"
)

UPLOAD_FOLDER = "uploads/medical_documents"

ALLOWED_EXTENSIONS = {
    "pdf",
    "png",
    "jpg",
    "jpeg"
}


os.makedirs(
    UPLOAD_FOLDER,
    exist_ok=True
)


def allowed_file(filename):

    return (
        "." in filename
        and
        filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS
    )


def save_document(file):

    if not file:
        return None

    if not allowed_file(file.filename):
        return None

    extension = (
        file.filename
        .rsplit(".", 1)[1]
        .lower()
    )

    filename = (
        f"{uuid.uuid4()}.{extension}"
    )

    filename = secure_filename(
        filename
    )

    filepath = os.path.join(
        UPLOAD_FOLDER,
        filename
    )

    file.save(filepath)

    return filepath

service = MedicalDocumentService()

access_control = AccessControlService()



# =====================================================
# UPLOAD DOCUMENT
# PROFESSIONAL ONLY
# =====================================================

@medical_document_bp.route(
    "/upload",
    methods=["POST"]
)
@jwt_required()
@role_required("professional")
def upload_document():

    user_id = get_jwt_identity()

    professional = (
        service.professional_model
        .get_by_user_id(
            user_id
        )
    )

    if not professional:

        return jsonify({

            "success": False,

            "message": "Professional profile not found."

        }), 404

    form = request.form

    uploaded_file = request.files.get(
        "file"
    )

    if not form:

        return jsonify({

            "success": False,

            "message": "Form data is required."

        }), 400

    patient_id = form.get(
        "patient_id"
    )

    if not patient_id or not uploaded_file:

        return jsonify({

            "success": False,

            "message": (
                "patient_id and file are required."
            )

        }), 400

    saved_path = save_document(
        uploaded_file
    )

    if not saved_path:

        return jsonify({

            "success": False,

            "message": "Invalid file type."

        }), 400

    result = service.upload_document(

        user_id,

        patient_id,

        uploaded_file.filename,

        form.get("document_type"),

        saved_path

    )

    if not result["success"]:

        return jsonify(result), 400

    return jsonify(result), 201

# =====================================================
# GET PATIENT DOCUMENTS
# =====================================================

@medical_document_bp.route(
    "/patient/<int:patient_id>",
    methods=["GET"]
)
@jwt_required()
def get_patient_documents(
        patient_id
):


    user_id = get_jwt_identity()



    allowed = False



    # ADMIN

    if access_control.is_administrator(
        user_id
    ):

        allowed = True




    # PATIENT

    elif access_control.can_access_patient(
        user_id,
        patient_id
    ):

        allowed = True




    # PROFESSIONAL

    else:


        professional = (
            service.professional_model
            .get_by_user_id(
                user_id
            )
        )


        if professional:


            relationship = (
                service.relationship_model
                .relationship_exists(

                    patient_id,

                    professional["id"]

                )
            )


            if relationship:

                allowed = True





    if not allowed:

        return jsonify({

            "success": False,

            "message": "Access denied."

        }), 403





    result = (
        service.get_patient_documents(
            patient_id
        )
    )


    return jsonify(result), 200







# =====================================================
# GET ALL DOCUMENTS
# ADMIN ONLY
# =====================================================

@medical_document_bp.route(
    "/all",
    methods=["GET"]
)
@jwt_required()
@role_required("administrator")
def get_all_documents():



    result = (
        service.get_all_documents()
    )



    return jsonify(result), 200







# =====================================================
# DELETE DOCUMENT
# ADMIN ONLY
# =====================================================

@medical_document_bp.route(
    "/<int:document_id>",
    methods=["DELETE"]
)
@jwt_required()
@role_required("administrator")
def delete_document(
        document_id
):



    result = (
        service.delete_document(
            document_id
        )
    )



    if not result["success"]:

        return jsonify(result), 404




    return jsonify(result), 200