from flask import Blueprint, jsonify

from flask_jwt_extended import (
    jwt_required,
    get_jwt_identity
)

from services.notifications.notification_service import NotificationService

from database.notifications.notification_model import NotificationModel



notification_bp = Blueprint(
    "notification",
    __name__,
    url_prefix="/notifications"
)



service = NotificationService()

model = NotificationModel()



# =====================================================
# GET MY NOTIFICATIONS
# =====================================================

@notification_bp.route(
    "/my",
    methods=["GET"]
)
@jwt_required()
def get_my_notifications():


    user_id = get_jwt_identity()


    result = service.get_user_notifications(
        user_id
    )


    if not result["success"]:

        return jsonify(result), 404



    return jsonify(result), 200





# =====================================================
# MARK NOTIFICATION AS READ
# =====================================================

@notification_bp.route(
    "/<int:notification_id>/read",
    methods=["PUT"]
)
@jwt_required()
def mark_as_read(notification_id):


    user_id = get_jwt_identity()


    notification = (
        model.get_by_user(
            user_id
        )
    )


    allowed = False


    for item in notification:

        if item["id"] == notification_id:

            allowed = True

            break



    if not allowed:

        return jsonify({

            "success": False,

            "message": "Access denied."

        }), 403





    result = service.mark_as_read(
        notification_id
    )


    if not result["success"]:

        return jsonify(result), 404



    return jsonify(result), 200





# =====================================================
# DELETE NOTIFICATION
# =====================================================

@notification_bp.route(
    "/<int:notification_id>",
    methods=["DELETE"]
)
@jwt_required()
def delete_notification(notification_id):


    user_id = get_jwt_identity()


    notifications = (
        model.get_by_user(
            user_id
        )
    )


    allowed = False


    for item in notifications:

        if item["id"] == notification_id:

            allowed = True

            break



    if not allowed:

        return jsonify({

            "success": False,

            "message": "Access denied."

        }), 403




    result = service.delete_notification(
        notification_id
    )


    if not result["success"]:

        return jsonify(result), 404



    return jsonify(result), 200