
from database.bank import connect


class AppointmentModel:


    @staticmethod
    def create(
        patient_id,
        professional_id,
        appointment_date,
        appointment_reason=None,
        meeting_link=None,
        notes=None,
        status="pending"
    ):

        conn = connect()
        cursor = conn.cursor()


        cursor.execute("""
            INSERT INTO appointments (

                patient_id,

                professional_id,

                appointment_date,

                appointment_reason,

                status,

                meeting_link,

                notes

            )

            VALUES (?, ?, ?, ?, ?, ?, ?)

        """, (

            patient_id,

            professional_id,

            appointment_date,

            appointment_reason,

            status,

            meeting_link,

            notes

        ))


        conn.commit()


        appointment_id = cursor.lastrowid


        conn.close()


        return appointment_id



    @staticmethod
    def get_by_id(appointment_id):

        conn = connect()
        cursor = conn.cursor()


        cursor.execute("""
            SELECT *

            FROM appointments

            WHERE id = ?

        """, (
            appointment_id,
        ))


        appointment = cursor.fetchone()


        conn.close()


        return appointment





    @staticmethod
    def get_by_patient(patient_id):

        conn = connect()
        cursor = conn.cursor()


        cursor.execute("""
            SELECT *

            FROM appointments

            WHERE patient_id = ?

            ORDER BY appointment_date DESC

        """, (
            patient_id,
        ))


        appointments = cursor.fetchall()


        conn.close()


        return appointments





    @staticmethod
    def get_by_professional(professional_id):

        conn = connect()
        cursor = conn.cursor()


        cursor.execute("""
            SELECT *

            FROM appointments

            WHERE professional_id = ?

            ORDER BY appointment_date DESC

        """, (
            professional_id,
        ))


        appointments = cursor.fetchall()


        conn.close()


        return appointments





    @staticmethod
    def get_all():

        conn = connect()
        cursor = conn.cursor()


        cursor.execute("""
            SELECT *

            FROM appointments

            ORDER BY appointment_date DESC

        """)


        appointments = cursor.fetchall()


        conn.close()


        return appointments





    @staticmethod
    def update_status(
        appointment_id,
        status
    ):

        conn = connect()
        cursor = conn.cursor()


        cursor.execute("""
            UPDATE appointments

            SET status = ?

            WHERE id = ?

        """, (

            status,

            appointment_id

        ))


        conn.commit()


        rows_updated = cursor.rowcount


        conn.close()


        return rows_updated





    @staticmethod
    def delete(appointment_id):

        conn = connect()
        cursor = conn.cursor()


        cursor.execute("""
            DELETE FROM appointments

            WHERE id = ?

        """, (
            appointment_id,
        ))


        conn.commit()


        rows_deleted = cursor.rowcount


        conn.close()


        return rows_deleted

    @staticmethod
    def appointment_exists(
            patient_id,
            professional_id,
            appointment_date
    ):
        conn = connect()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT *

            FROM appointments

            WHERE patient_id = ?

            AND professional_id = ?

            AND appointment_date = ?

            AND status != 'cancelled'

        """, (

            patient_id,

            professional_id,

            appointment_date

        ))

        appointment = cursor.fetchone()

        conn.close()

        return appointment

