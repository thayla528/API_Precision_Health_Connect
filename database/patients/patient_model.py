from database.bank import connect


class PatientModel:


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
    def get_next_appointment(user_id):

        conn = connect()
        cursor = conn.cursor()

        cursor.execute("""
                SELECT

                    a.id,
                    a.appointment_date,
                    a.status,

                    u.full_name AS professional,
                    pr.specialty


                FROM appointments a


                JOIN professionals pr
                    ON a.professional_id = pr.id


                JOIN users u
                    ON pr.user_id = u.id


                JOIN patients pt
                    ON a.patient_id = pt.id


                WHERE pt.user_id = ?


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

                u.full_name AS professional,

                p.specialty


            FROM appointments a


            JOIN patients pt
                ON a.patient_id = pt.id


            JOIN professionals p
                ON a.professional_id = p.id


            JOIN users u
                ON p.user_id = u.id


            WHERE pt.user_id = ?


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

                u.full_name AS professional,

                p.specialty


            FROM appointments a


            JOIN patients pt
                ON a.patient_id = pt.id


            JOIN professionals p
                ON a.professional_id = p.id


            JOIN users u
                ON p.user_id = u.id


            WHERE pt.user_id = ?


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
    def get_documents(user_id):

        conn = connect()
        cursor = conn.cursor()


        cursor.execute("""

            SELECT

                file_name,
                document_type,
                uploaded_at


            FROM medical_documents


            WHERE patient_id = (

                SELECT id

                FROM patients

                WHERE user_id = ?

            )


            ORDER BY uploaded_at DESC


            LIMIT 5


        """,(user_id,))


        documents = cursor.fetchall()


        conn.close()


        return [
            dict(item)
            for item in documents
        ]

    @staticmethod
    def get_notifications(user_id):

        conn = connect()
        cursor = conn.cursor()


        cursor.execute("""

            SELECT

                title,
                message,
                sent_at


            FROM notifications


            WHERE user_id = ?


            ORDER BY sent_at DESC


            LIMIT 5


        """,(user_id,))


        notifications = cursor.fetchall()


        conn.close()


        return [
            dict(item)
            for item in notifications
        ]

    @staticmethod
    def count_messages(user_id):

        conn = connect()
        cursor = conn.cursor()


        cursor.execute("""

            SELECT COUNT(*) as total

            FROM messages

            WHERE receiver_id = ?

            AND is_read = 0


        """,(user_id,))


        result = cursor.fetchone()


        conn.close()


        return result["total"]

    @staticmethod
    def count_notifications(user_id):

        conn = connect()
        cursor = conn.cursor()


        cursor.execute("""

            SELECT COUNT(*) as total

            FROM notifications

            WHERE user_id = ?

            AND is_read = 0


        """,(user_id,))


        result = cursor.fetchone()


        conn.close()


        return result["total"]

    @staticmethod
    def count_pending_exams(user_id):

        conn = connect()
        cursor = conn.cursor()

        cursor.execute("""

            SELECT COUNT(*) AS total

            FROM exams e

            JOIN patients p
                ON e.patient_id = p.id

            WHERE p.user_id = ?

            AND e.status = 'pending'


        """, (user_id,))

        result = cursor.fetchone()

        conn.close()

        return result["total"]

    @staticmethod
    def get_timeline(user_id):

        conn = connect()
        cursor = conn.cursor()

        cursor.execute("""

            SELECT

                'CONSULTA' AS type,

                u.full_name AS title,

                a.appointment_date AS date


            FROM appointments a


            JOIN patients p
                ON a.patient_id = p.id


            JOIN professionals pr
                ON a.professional_id = pr.id


            JOIN users u
                ON pr.user_id = u.id


            WHERE p.user_id = ?



            UNION ALL



            SELECT

                'DOCUMENTO' AS type,

                document_type AS title,

                uploaded_at AS date


            FROM medical_documents d


            JOIN patients p
                ON d.patient_id = p.id


            WHERE p.user_id = ?



            ORDER BY date DESC


            LIMIT 10


        """, (user_id, user_id))

        data = cursor.fetchall()

        conn.close()

        return [
            dict(item)
            for item in data
        ]

    @staticmethod
    def get_health_summary(user_id):

        conn = connect()
        cursor = conn.cursor()

        cursor.execute("""

            SELECT COUNT(*) AS total

            FROM appointments a

            JOIN patients p
                ON a.patient_id = p.id

            WHERE p.user_id = ?


        """, (user_id,))

        consultations = cursor.fetchone()["total"]

        cursor.execute("""

            SELECT COUNT(*) AS total

            FROM exams e

            JOIN patients p
                ON e.patient_id = p.id

            WHERE p.user_id = ?


        """, (user_id,))

        exams = cursor.fetchone()["total"]

        cursor.execute("""

            SELECT COUNT(*) AS total

            FROM medications m

            JOIN patients p
                ON m.patient_id = p.id

            WHERE p.user_id = ?

            AND m.active = 1


        """, (user_id,))

        medications = cursor.fetchone()["total"]

        cursor.execute("""

            SELECT COUNT(*) AS total

            FROM vaccines v

            JOIN patients p
                ON v.patient_id = p.id


            WHERE p.user_id = ?


        """, (user_id,))

        vaccines = cursor.fetchone()["total"]

        conn.close()

        # Metas fictícias (podem ser alteradas depois)
        consultation_goal = 10
        exam_goal = 10
        medication_goal = 5
        vaccine_goal = 5

        return {

            "consultations": min(round((consultations / consultation_goal) * 100), 100),

            "exams": min(round((exams / exam_goal) * 100), 100),

            "medications": min(round((medications / medication_goal) * 100), 100),

            "vaccines": min(round((vaccines / vaccine_goal) * 100), 100)

        }

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


                p.cpf,
                p.gender,
                p.blood_type,

                p.postal_code,
                p.address,
                p.house_number,
                p.address_line2,
                p.neighborhood,
                p.city,
                p.state,

                p.notes


            FROM users u


            JOIN patients p

                ON p.user_id = u.id


            WHERE u.id = ?


        """, (user_id,))

        profile = cursor.fetchone()

        conn.close()

        if profile:
            return dict(profile)

        return {}