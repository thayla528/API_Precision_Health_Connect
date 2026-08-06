from database.notifications.notification_model import NotificationModel

from database.users.user_model import UserModel



class NotificationService:


    def __init__(self):

        self.notification_model = NotificationModel()

        self.user_model = UserModel()



    # =====================================================
    # CREATE NOTIFICATION
    # =====================================================

    def create_notification(
            self,
            user_id,
            title,
            message,
            notification_type=None
    ):


        user = self.user_model.get_by_id(
            user_id
        )


        if not user:

            return {

                "success": False,

                "message": "User not found."

            }




        notification_id = (
            self.notification_model
            .create(
                user_id,
                title,
                message,
                notification_type
            )
        )



        return {

            "success": True,

            "message": "Notification created successfully.",

            "notification_id": notification_id

        }





    # =====================================================
    # GET USER NOTIFICATIONS
    # =====================================================

    def get_user_notifications(
            self,
            user_id
    ):


        user = self.user_model.get_by_id(
            user_id
        )


        if not user:

            return {

                "success": False,

                "message": "User not found."

            }



        notifications = (
            self.notification_model
            .get_by_user(
                user_id
            )
        )



        return {

            "success": True,

            "notifications": [

                dict(item)

                for item in notifications

            ]

        }





    # =====================================================
    # MARK AS READ
    # =====================================================

    def mark_as_read(
            self,
            notification_id
    ):


        updated = (
            self.notification_model
            .mark_as_read(
                notification_id
            )
        )



        if updated == 0:

            return {

                "success": False,

                "message": "Notification not found."

            }




        return {

            "success": True,

            "message": "Notification marked as read."

        }





    # =====================================================
    # DELETE NOTIFICATION
    # =====================================================

    def delete_notification(
            self,
            notification_id
    ):


        deleted = (
            self.notification_model
            .delete(
                notification_id
            )
        )



        if deleted == 0:

            return {

                "success": False,

                "message": "Notification not found."

            }



        return {

            "success": True,

            "message": "Notification deleted successfully."

        }