from database.bank import connect



class NotificationModel:


    @staticmethod
    def create(
            user_id,
            title,
            message,
            notification_type=None
    ):

        conn = connect()
        cursor = conn.cursor()


        cursor.execute("""
            INSERT INTO notifications (

                user_id,

                type,

                title,

                message

            )

            VALUES (?, ?, ?, ?)

        """, (

            user_id,

            notification_type,

            title,

            message

        ))


        conn.commit()


        notification_id = cursor.lastrowid


        conn.close()


        return notification_id



    @staticmethod
    def get_by_user(user_id):

        conn = connect()
        cursor = conn.cursor()


        cursor.execute("""
            SELECT *

            FROM notifications

            WHERE user_id = ?

            ORDER BY sent_at DESC

        """, (

            user_id,

        ))


        notifications = cursor.fetchall()


        conn.close()


        return notifications



    @staticmethod
    def mark_as_read(notification_id):

        conn = connect()
        cursor = conn.cursor()


        cursor.execute("""
            UPDATE notifications

            SET is_read = 1

            WHERE id = ?

        """, (

            notification_id,

        ))


        conn.commit()


        updated = cursor.rowcount


        conn.close()


        return updated



    @staticmethod
    def delete(notification_id):

        conn = connect()
        cursor = conn.cursor()


        cursor.execute("""
            DELETE FROM notifications

            WHERE id = ?

        """, (

            notification_id,

        ))


        conn.commit()


        deleted = cursor.rowcount


        conn.close()


        return deleted