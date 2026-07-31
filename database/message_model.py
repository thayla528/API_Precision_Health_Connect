from database.bank import connect

#

class MessageModel:

    @staticmethod
    def send_message(sender_id, receiver_id, message):
        conn = connect()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO messages (
                sender_id,
                receiver_id,
                message
            )
            VALUES (?, ?, ?)
        """, (
            sender_id,
            receiver_id,
            message
        ))

        conn.commit()

        message_id = cursor.lastrowid

        conn.close()

        return message_id

    @staticmethod
    def get_received_messages(user_id):
        conn = connect()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT
                m.id,
                m.sender_id,
                u.full_name AS sender_name,
                m.message,
                m.is_read,
                m.sent_at
            FROM messages m

            JOIN users u
                ON m.sender_id = u.id

            WHERE m.receiver_id = ?

            ORDER BY m.sent_at DESC
        """, (user_id,))

        messages = cursor.fetchall()

        conn.close()

        return [
            dict(message)
            for message in messages
        ]

    @staticmethod
    def get_conversation(user1_id, user2_id):
        conn = connect()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT
                m.id,
                m.sender_id,
                sender.full_name AS sender_name,

                m.receiver_id,
                receiver.full_name AS receiver_name,

                m.message,
                m.is_read,
                m.sent_at

            FROM messages m

            JOIN users sender
                ON m.sender_id = sender.id

            JOIN users receiver
                ON m.receiver_id = receiver.id

            WHERE
                (m.sender_id = ? AND m.receiver_id = ?)
                OR
                (m.sender_id = ? AND m.receiver_id = ?)

            ORDER BY m.sent_at ASC
        """, (
            user1_id,
            user2_id,
            user2_id,
            user1_id
        ))

        messages = cursor.fetchall()

        conn.close()

        return [
            dict(message)
            for message in messages
        ]

    @staticmethod
    def mark_as_read(message_id):
        conn = connect()
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE messages
            SET is_read = 1
            WHERE id = ?
        """, (message_id,))

        conn.commit()

        rows_updated = cursor.rowcount

        conn.close()

        return rows_updated