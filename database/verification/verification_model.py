from database.bank import connect


class VerificationModel:

    @staticmethod
    def create(
        email,
        phone,
        email_code,
        phone_code,
        email_expires_at,
        phone_expires_at
    ):

        conn = connect()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO verifications (
                email,
                phone,
                email_code,
                phone_code,
                email_expires_at,
                phone_expires_at
            )
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            email,
            phone,
            email_code,
            phone_code,
            email_expires_at,
            phone_expires_at
        ))

        conn.commit()

        verification_id = cursor.lastrowid

        conn.close()

        return verification_id


    @staticmethod
    def get_by_id(verification_id):

        conn = connect()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT *
            FROM verifications
            WHERE id = ?
        """, (verification_id,))

        verification = cursor.fetchone()

        conn.close()

        return verification


    @staticmethod
    def get_latest_by_email(email):

        conn = connect()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT *
            FROM verifications
            WHERE email = ?
            ORDER BY created_at DESC
            LIMIT 1
        """, (email,))

        verification = cursor.fetchone()

        conn.close()

        return verification


    @staticmethod
    def mark_email_verified(verification_id):

        conn = connect()
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE verifications
            SET email_verified = 1
            WHERE id = ?
        """, (verification_id,))

        conn.commit()

        conn.close()


    @staticmethod
    def mark_phone_verified(verification_id):

        conn = connect()
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE verifications
            SET phone_verified = 1
            WHERE id = ?
        """, (verification_id,))

        conn.commit()

        conn.close()


    @staticmethod
    def delete(verification_id):

        conn = connect()
        cursor = conn.cursor()

        cursor.execute("""
            DELETE FROM verifications
            WHERE id = ?
        """, (verification_id,))

        conn.commit()

        conn.close()