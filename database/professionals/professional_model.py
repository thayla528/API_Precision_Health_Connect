
from database.bank import connect


class ProfessionalModel:

    # =====================================================
    # CREATE
    # =====================================================

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


    # =====================================================
    # GET USER
    # =====================================================

    @staticmethod
    def get_user(user_id):

        conn = connect()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT
                id,
                full_name,
                email,
                role,
                profile_type,
                profile_photo,
                active,
                last_login,
                created_at
            FROM users
            WHERE id = ?
        """, (user_id,))

        user = cursor.fetchone()

        conn.close()

        if user:
            return dict(user)

        return None


    # =====================================================
    # GET PROFESSIONAL PROFILE
    # =====================================================

    @staticmethod
    def get_profile(user_id):

        conn = connect()
        cursor = conn.cursor()

        cursor.execute("""

            SELECT

                -- USERS

                u.id,
                u.id AS user_id,
                u.full_name,
                u.email,
                u.role,
                u.profile_type,
                u.profile_photo,
                u.active AS user_active,
                u.last_login,
                u.created_at AS user_created_at,

                -- PROFESSIONALS

                p.id AS professional_id,
                p.specialty,
                p.license_number,
                p.institution,
                p.practice_area,
                p.phone,
                p.professional_email,
                p.active AS professional_active,
                p.created_at AS professional_created_at

            FROM users u

            JOIN professionals p
                ON p.user_id = u.id

            WHERE u.id = ?

        """, (user_id,))

        profile = cursor.fetchone()

        conn.close()

        if profile:
            return dict(profile)

        return None


    # =====================================================
    # UPDATE USER DATA
    # =====================================================

    @staticmethod
    def update_user(
            user_id,
            full_name=None,
            email=None,
            password=None,
            profile_photo=None
    ):

        conn = connect()
        cursor = conn.cursor()

        fields = []
        values = []


        if full_name is not None:

            fields.append(
                "full_name = ?"
            )

            values.append(full_name)


        if email is not None:

            fields.append(
                "email = ?"
            )

            values.append(email)


        if password is not None:

            fields.append(
                "password = ?"
            )

            values.append(password)


        if profile_photo is not None:

            fields.append(
                "profile_photo = ?"
            )

            values.append(profile_photo)


        if not fields:

            conn.close()

            return True


        values.append(user_id)


        cursor.execute(
            f"""
            UPDATE users
            SET {", ".join(fields)}
            WHERE id = ?
            """,
            values
        )


        conn.commit()

        conn.close()

        return True


    # =====================================================
    # UPDATE PROFESSIONAL DATA
    # =====================================================

    @staticmethod
    def update_profile(
            user_id,
            specialty=None,
            license_number=None,
            institution=None,
            practice_area=None,
            phone=None,
            professional_email=None
    ):

        conn = connect()
        cursor = conn.cursor()

        fields = []
        values = []


        if specialty is not None:

            fields.append(
                "specialty = ?"
            )

            values.append(specialty)


        if license_number is not None:

            fields.append(
                "license_number = ?"
            )

            values.append(license_number)


        if institution is not None:

            fields.append(
                "institution = ?"
            )

            values.append(institution)


        if practice_area is not None:

            fields.append(
                "practice_area = ?"
            )

            values.append(practice_area)


        if phone is not None:

            fields.append(
                "phone = ?"
            )

            values.append(phone)


        if professional_email is not None:

            fields.append(
                "professional_email = ?"
            )

            values.append(professional_email)


        if not fields:

            conn.close()

            return True


        values.append(user_id)


        cursor.execute(
            f"""
            UPDATE professionals

            SET {", ".join(fields)}

            WHERE user_id = ?
            """,
            values
        )


        conn.commit()

        conn.close()

        return True


    # =====================================================
    # GET NEXT APPOINTMENT
    # =====================================================

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


    # =====================================================
    # GET RECENT APPOINTMENTS
    # =====================================================

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


    # =====================================================
    # GET UPCOMING APPOINTMENTS
    # =====================================================

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


    # =====================================================
    # COUNT MESSAGES
    # =====================================================

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


    # =====================================================
    # COUNT NOTIFICATIONS
    # =====================================================

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

