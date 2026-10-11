from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from security.permissions import role_required
from database.patients.patient_entity_model import PatientEntityModel
from database.professionals.professional_entity_model import ProfessionalEntityModel
from services.exam.exam_service import ExamService
from services.security_service.access_control_service import AccessControlService


exam_bp = Blueprint("exam", __name__, url_prefix="/exams")
service = ExamService()
access_control = AccessControlService()
patient_model = PatientEntityModel()
professional_model = ProfessionalEntityModel()


@exam_bp.route("/create", methods=["POST"])
@jwt_required()
@role_required("professional")
def create_exam():
    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        return jsonify({"success": False, "message": "JSON body is required."}), 400
    patient_id = data.get("patient_id")
    if not patient_id:
        return jsonify({"success": False, "message": "patient_id is required."}), 400
    result = service.create_exam(get_jwt_identity(), patient_id, data)
    return jsonify(result), 201 if result["success"] else 400


@exam_bp.route("/my", methods=["GET"])
@jwt_required()
def my_exams():
    user_id = get_jwt_identity()

    if access_control.is_administrator(user_id):
        return jsonify(service.get_all_exams()), 200

    patient = patient_model.get_by_user_id(user_id)
    if patient:
        return jsonify(service.get_patient_exams(patient["id"])), 200

    professional = professional_model.get_by_user_id(user_id)
    if professional:
        return jsonify(service.get_professional_exams(professional["id"])), 200

    return jsonify({"success": False, "message": "Profile not found."}), 404


@exam_bp.route("/<int:exam_id>", methods=["GET"])
@jwt_required()
def get_exam(exam_id):
    user_id = get_jwt_identity()
    exam = service.get_exam(exam_id)
    if not exam:
        return jsonify({"success": False, "message": "Exam not found."}), 404

    allowed = access_control.is_administrator(user_id)
    patient = patient_model.get_by_user_id(user_id)
    professional = professional_model.get_by_user_id(user_id)

    if patient and patient["id"] == exam["patient_id"]:
        allowed = True
    if professional and professional["id"] == exam["professional_id"]:
        allowed = True

    if not allowed:
        return jsonify({"success": False, "message": "Access denied."}), 403

    return jsonify({"success": True, "exam": exam}), 200


@exam_bp.route("/<int:exam_id>/status", methods=["PUT"])
@jwt_required()
def update_exam_status(exam_id):
    user_id = get_jwt_identity()
    exam = service.get_exam(exam_id)
    if not exam:
        return jsonify({"success": False, "message": "Exam not found."}), 404

    is_admin = access_control.is_administrator(user_id)
    professional = professional_model.get_by_user_id(user_id)
    if not is_admin and (not professional or professional["id"] != exam["professional_id"]):
        return jsonify({"success": False, "message": "Access denied."}), 403

    data = request.get_json(silent=True)
    if not isinstance(data, dict) or not data.get("status"):
        return jsonify({"success": False, "message": "status is required."}), 400
    result = service.update_status(exam_id, data["status"])
    return jsonify(result), 200 if result["success"] else 400


@exam_bp.route("/<int:exam_id>/schedule", methods=["PUT"])
@jwt_required()
def schedule_exam(exam_id):
    user_id = get_jwt_identity()
    exam = service.get_exam(exam_id)
    if not exam:
        return jsonify({"success": False, "message": "Exam not found."}), 404

    is_admin = access_control.is_administrator(user_id)
    professional = professional_model.get_by_user_id(user_id)
    if not is_admin and (not professional or professional["id"] != exam["professional_id"]):
        return jsonify({"success": False, "message": "Access denied."}), 403

    data = request.get_json(silent=True)
    if not isinstance(data, dict) or not data.get("scheduled_at"):
        return jsonify({"success": False, "message": "scheduled_at is required."}), 400
    result = service.schedule_exam(exam_id, data["scheduled_at"], data.get("institution_id"))
    return jsonify(result), 200 if result["success"] else 400


@exam_bp.route("/<int:exam_id>/result", methods=["PUT"])
@jwt_required()
def attach_exam_result(exam_id):
    user_id = get_jwt_identity()
    exam = service.get_exam(exam_id)
    if not exam:
        return jsonify({"success": False, "message": "Exam not found."}), 404

    is_admin = access_control.is_administrator(user_id)
    professional = professional_model.get_by_user_id(user_id)
    if not is_admin and (not professional or professional["id"] != exam["professional_id"]):
        return jsonify({"success": False, "message": "Access denied."}), 403

    data = request.get_json(silent=True)
    if not isinstance(data, dict) or not data.get("result_document_id"):
        return jsonify({"success": False, "message": "result_document_id is required."}), 400
    result = service.attach_result_document(exam_id, data["result_document_id"])
    return jsonify(result), 200 if result["success"] else 400
