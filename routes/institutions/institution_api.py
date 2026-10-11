from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from security.permissions import role_required
from database.institutions.institution_model import InstitutionModel
from database.professionals.professional_entity_model import ProfessionalEntityModel
from services.institutions.institution_service import InstitutionService
from services.security_service.access_control_service import AccessControlService


institution_bp = Blueprint("institution", __name__, url_prefix="/institutions")
service = InstitutionService()
access_control = AccessControlService()
institution_model = InstitutionModel()
professional_model = ProfessionalEntityModel()


@institution_bp.route("/", methods=["GET"])
@jwt_required()
def list_institutions():
    result = service.get_active_institutions()
    return jsonify(result), 200


@institution_bp.route("/nearby", methods=["GET"])
@jwt_required()
def nearby_institutions():
    latitude = request.args.get("latitude")
    longitude = request.args.get("longitude")
    radius_km = request.args.get("radius_km", 25)
    result = service.nearby(latitude, longitude, radius_km)
    if not result["success"]:
        return jsonify(result), 400
    return jsonify(result), 200


@institution_bp.route("/<int:institution_id>", methods=["GET"])
@jwt_required()
def get_institution(institution_id):
    institution = institution_model.get_by_id(institution_id)
    if not institution or not institution["active"]:
        return jsonify({"success": False, "message": "Institution not found."}), 404
    return jsonify({"success": True, "institution": dict(institution)}), 200


@institution_bp.route("/create", methods=["POST"])
@jwt_required()
@role_required("administrator")
def create_institution():
    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        return jsonify({"success": False, "message": "JSON body is required."}), 400
    result = service.create_institution(data)
    return jsonify(result), 201 if result["success"] else 400


@institution_bp.route("/<int:institution_id>/professionals/<int:professional_id>", methods=["POST"])
@jwt_required()
@role_required("administrator")
def link_professional(institution_id, professional_id):
    data = request.get_json(silent=True) or {}
    result = service.link_professional(
        professional_id,
        institution_id,
        data.get("is_primary", False)
    )
    return jsonify(result), 200 if result["success"] else 400


@institution_bp.route("/<int:institution_id>/professionals/<int:professional_id>", methods=["DELETE"])
@jwt_required()
@role_required("administrator")
def unlink_professional(institution_id, professional_id):
    institution = institution_model.get_by_id(institution_id)
    professional = professional_model.get_by_id(professional_id)
    if not institution or not professional:
        return jsonify({"success": False, "message": "Institution or professional not found."}), 404
    changed = institution_model.unlink_professional(professional_id, institution_id)
    if not changed:
        return jsonify({"success": False, "message": "Active professional-institution link not found."}), 404
    return jsonify({"success": True, "message": "Professional unlinked from institution."}), 200


@institution_bp.route("/my", methods=["GET"])
@jwt_required()
def my_institutions():
    user_id = get_jwt_identity()
    professional = professional_model.get_by_user_id(user_id)
    if not professional:
        if access_control.is_administrator(user_id):
            return jsonify(service.get_active_institutions()), 200
        return jsonify({"success": False, "message": "Professional profile not found."}), 404
    rows = institution_model.get_by_professional(professional["id"])
    return jsonify({"success": True, "institutions": [dict(row) for row in rows]}), 200
