from database.bank import connect


class PatientEntityModel:

    @staticmethod
    def create(user_id):
        conn = connect()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO patients (
                user_id
            )
            VALUES (?)
        """, (
            user_id,
        ))

        conn.commit()

        patient_id = cursor.lastrowid

        conn.close()

        return patient_id


    @staticmethod
    def get_by_id(patient_id):

        conn = connect()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT *
            FROM patients
            WHERE id = ?
        """, (patient_id,))

        patient = cursor.fetchone()

        conn.close()

        return patient


    @staticmethod
    def get_by_user_id(user_id):

        conn = connect()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT *
            FROM patients
            WHERE user_id = ?
        """, (user_id,))

        patient = cursor.fetchone()

        conn.close()

        return patient