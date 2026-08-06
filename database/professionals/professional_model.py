from database.bank import connect


class ProfessionalModel:

    @staticmethod
    def create(
            user_id,
            specialty,
            license_number,
            institution=None,
            practice_area=None,
            phone=None,
            professional_email=None
    ):

        conn = connect()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO professionals (
                user_id,
                specialty,
                license_number,
                institution,
                practice_area,
                phone,
                professional_email
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            user_id,
            specialty,
            license_number,
            institution,
            practice_area,
            phone,
            professional_email
        ))

        conn.commit()

        professional_id = cursor.lastrowid

        conn.close()

        return professional_id

    @staticmethod
    def get_user(user_id):

        conn = connect()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT
                id,
                full_name,
                email,
                profile_type,
                profile_photo
            FROM users
            WHERE id = ?
        """, (user_id,))

        user = cursor.fetchone()

        conn.close()

        if user:
            return dict(user)

        return None


    @staticmethod
    def get_profile(user_id):

        conn = connect()
        cursor = conn.cursor()

        cursor.execute("""

            SELECT

                u.id,
                u.full_name,
                u.email,
                u.profile_photo,
                u.created_at,

                p.specialty,
                p.license_number,
                p.institution,
                p.practice_area,
                p.phone,
                p.professional_email,
                p.active

            FROM users u

            JOIN professionals p
                ON p.user_id = u.id

            WHERE u.id = ?

        """, (user_id,))

        profile = cursor.fetchone()

        conn.close()

        if profile:
            return dict(profile)

        return {}


    @staticmethod
    def get_next_appointment(user_id):

        conn = connect()
        cursor = conn.cursor()

        cursor.execute("""

            SELECT

                a.id,
                a.appointment_date,
                a.status,

                u.full_name AS patient

            FROM appointments a

            JOIN professionals pr
                ON a.professional_id = pr.id

            JOIN patients pt
                ON a.patient_id = pt.id

            JOIN users u
                ON pt.user_id = u.id

            WHERE pr.user_id = ?

            ORDER BY a.appointment_date ASC

            LIMIT 1

        """, (user_id,))

        appointment = cursor.fetchone()

        conn.close()

        if appointment:
            return dict(appointment)

        return None


    @staticmethod
    def get_recent_appointments(user_id):

        conn = connect()
        cursor = conn.cursor()

        cursor.execute("""

            SELECT

                a.appointment_date,
                a.status,

                u.full_name AS patient

            FROM appointments a

            JOIN professionals pr
                ON a.professional_id = pr.id

            JOIN patients pt
                ON a.patient_id = pt.id

            JOIN users u
                ON pt.user_id = u.id

            WHERE pr.user_id = ?

            ORDER BY a.appointment_date DESC

            LIMIT 5

        """, (user_id,))

        data = cursor.fetchall()

        conn.close()

        return [
            dict(item)
            for item in data
        ]


    @staticmethod
    def get_upcoming_appointments(user_id):

        conn = connect()
        cursor = conn.cursor()

        cursor.execute("""

            SELECT

                a.appointment_date,

                u.full_name AS patient

            FROM appointments a

            JOIN professionals pr
                ON a.professional_id = pr.id

            JOIN patients pt
                ON a.patient_id = pt.id

            JOIN users u
                ON pt.user_id = u.id

            WHERE pr.user_id = ?

            AND a.appointment_date >= CURRENT_TIMESTAMP

            ORDER BY a.appointment_date ASC

            LIMIT 5

        """, (user_id,))

        data = cursor.fetchall()

        conn.close()

        return [
            dict(item)
            for item in data
        ]


    @staticmethod
    def count_messages(user_id):

        conn = connect()
        cursor = conn.cursor()

        cursor.execute("""

            SELECT COUNT(*) AS total

            FROM messages

            WHERE receiver_id = ?

            AND is_read = 0

        """, (user_id,))

        result = cursor.fetchone()

        conn.close()

        return result["total"]


    @staticmethod
    def count_notifications(user_id):

        conn = connect()
        cursor = conn.cursor()

        cursor.execute("""

            SELECT COUNT(*) AS total

            FROM notifications

            WHERE user_id = ?

            AND is_read = 0

        """, (user_id,))

        result = cursor.fetchone()

        conn.close()

        return result["total"]