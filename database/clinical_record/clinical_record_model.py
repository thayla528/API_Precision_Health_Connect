from database.bank import connect


class ClinicalRecordModel:


    @staticmethod
    def create(
        appointment_id,
        diagnosis=None,
        treatment=None,
        prescription=None,
        notes=None
    ):

        conn = connect()
        cursor = conn.cursor()


        cursor.execute("""
            INSERT INTO clinical_records (

                appointment_id,

                diagnosis,

                treatment,

                prescription,

                notes

            )

            VALUES (?, ?, ?, ?, ?)

        """, (

            appointment_id,

            diagnosis,

            treatment,

            prescription,

            notes

        ))


        conn.commit()


        record_id = cursor.lastrowid


        conn.close()


        return record_id



    @staticmethod
    def get_by_id(record_id):

        conn = connect()
        cursor = conn.cursor()


        cursor.execute("""
            SELECT *
            FROM clinical_records
            WHERE id = ?

        """, (
            record_id,
        ))


        record = cursor.fetchone()


        conn.close()


        return record

    @staticmethod
    def update(
            record_id,
            diagnosis,
            treatment,
            prescription,
            notes
    ):
        conn = connect()
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE clinical_records

            SET

                diagnosis = ?,

                treatment = ?,

                prescription = ?,

                notes = ?

            WHERE id = ?

        """, (

            diagnosis,

            treatment,

            prescription,

            notes,

            record_id

        ))

        conn.commit()

        rows_updated = cursor.rowcount

        conn.close()

        return rows_updated



    @staticmethod
    def get_by_appointment(
            appointment_id
    ):

        conn = connect()
        cursor = conn.cursor()


        cursor.execute("""
            SELECT *
            FROM clinical_records
            WHERE appointment_id = ?

        """, (
            appointment_id,
        ))


        records = cursor.fetchall()


        conn.close()


        return records



    @staticmethod
    def get_by_patient(
            patient_id
    ):

        conn = connect()
        cursor = conn.cursor()


        cursor.execute("""
            SELECT 
                clinical_records.*

            FROM clinical_records

            JOIN appointments

            ON clinical_records.appointment_id = appointments.id

            WHERE appointments.patient_id = ?

            ORDER BY recorded_at DESC

        """, (
            patient_id,
        ))


        records = cursor.fetchall()


        conn.close()


        return records



    @staticmethod
    def get_all():

        conn = connect()
        cursor = conn.cursor()


        cursor.execute("""
            SELECT *
            FROM clinical_records
            ORDER BY recorded_at DESC

        """)


        records = cursor.fetchall()


        conn.close()


        return records