from database.bank import connect


class PrescriptionModel:


    @staticmethod
    def create(
        patient_id,
        professional_id,
        appointment_id=None,
        medication=None,
        dosage=None,
        frequency=None,
        duration=None,
        prescription_type=None,
        instructions=None,
        status="pending"
    ):

        conn = connect()
        cursor = conn.cursor()


        cursor.execute("""
            INSERT INTO prescriptions (

                patient_id,

                professional_id,

                appointment_id,

                medication,

                dosage,

                frequency,

                duration,

                prescription_type,

                instructions,

                status

            )

            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)

        """, (

            patient_id,

            professional_id,

            appointment_id,

            medication,

            dosage,

            frequency,

            duration,

            prescription_type,

            instructions,

            status

        ))


        conn.commit()


        prescription_id = cursor.lastrowid


        conn.close()


        return prescription_id



    @staticmethod
    def get_by_id(prescription_id):

        conn = connect()
        cursor = conn.cursor()


        cursor.execute("""
            SELECT *
            FROM prescriptions
            WHERE id = ?

        """, (
            prescription_id,
        ))


        prescription = cursor.fetchone()


        conn.close()


        return prescription



    @staticmethod
    def update(
        prescription_id,
        medication,
        dosage,
        frequency,
        duration,
        prescription_type,
        instructions,
        status
    ):

        conn = connect()
        cursor = conn.cursor()


        cursor.execute("""
            UPDATE prescriptions

            SET

                medication = ?,

                dosage = ?,

                frequency = ?,

                duration = ?,

                prescription_type = ?,

                instructions = ?,

                status = ?

            WHERE id = ?

        """, (

            medication,

            dosage,

            frequency,

            duration,

            prescription_type,

            instructions,

            status,

            prescription_id

        ))


        conn.commit()


        rows_updated = cursor.rowcount


        conn.close()


        return rows_updated



    @staticmethod
    def get_by_patient(patient_id):

        conn = connect()
        cursor = conn.cursor()


        cursor.execute("""
            SELECT *
            FROM prescriptions

            WHERE patient_id = ?

            ORDER BY created_at DESC

        """, (
            patient_id,
        ))


        prescriptions = cursor.fetchall()


        conn.close()


        return prescriptions



    @staticmethod
    def get_by_professional(professional_id):

        conn = connect()
        cursor = conn.cursor()


        cursor.execute("""
            SELECT *
            FROM prescriptions

            WHERE professional_id = ?

            ORDER BY created_at DESC

        """, (
            professional_id,
        ))


        prescriptions = cursor.fetchall()


        conn.close()


        return prescriptions



    @staticmethod
    def get_by_appointment(appointment_id):

        conn = connect()
        cursor = conn.cursor()


        cursor.execute("""
            SELECT *
            FROM prescriptions

            WHERE appointment_id = ?

            ORDER BY created_at DESC

        """, (
            appointment_id,
        ))


        prescriptions = cursor.fetchall()


        conn.close()


        return prescriptions



    @staticmethod
    def get_all():

        conn = connect()
        cursor = conn.cursor()


        cursor.execute("""
            SELECT *
            FROM prescriptions

            ORDER BY created_at DESC

        """)


        prescriptions = cursor.fetchall()


        conn.close()


        return prescriptions