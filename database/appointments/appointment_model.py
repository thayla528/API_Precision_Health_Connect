from database.bank import connect


class AppointmentModel:

    # =====================================================
    # CREATE APPOINTMENT
    # =====================================================

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

        try:

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

            return appointment_id

        finally:

            conn.close()


    # =====================================================
    # GET APPOINTMENT BY ID
    # =====================================================

    @staticmethod
    def get_by_id(appointment_id):

        conn = connect()
        cursor = conn.cursor()

        try:

            cursor.execute("""
                SELECT *

                FROM appointments

                WHERE id = ?

            """, (
                appointment_id,
            ))

            appointment = cursor.fetchone()

            return appointment

        finally:

            conn.close()

    # =====================================================
    # GET APPOINTMENTS BY PATIENT
    # =====================================================

    @staticmethod
    def get_by_patient(patient_id):

        conn = connect()
        cursor = conn.cursor()

        try:

            cursor.execute("""
                           SELECT appointments.id,
                                  appointments.patient_id,
                                  appointments.professional_id,
                                  appointments.appointment_date,
                                  appointments.appointment_reason,
                                  appointments.status,
                                  appointments.meeting_link,
                                  appointments.notes,
                                  appointments.created_at,

                                  users.full_name     AS professional_name,
                                  users.profile_photo AS professional_photo,

                                  professionals.specialty

                           FROM appointments

                                    INNER JOIN professionals
                                               ON professionals.id = appointments.professional_id

                                    INNER JOIN users
                                               ON users.id = professionals.user_id

                           WHERE appointments.patient_id = ?

                           ORDER BY appointments.appointment_date ASC

                           """, (
                               patient_id,
                           ))

            appointments = cursor.fetchall()

            return appointments

        finally:

            conn.close()

    # =====================================================
    # GET APPOINTMENTS BY PROFESSIONAL
    # =====================================================

    @staticmethod
    def get_by_professional(professional_id):

        conn = connect()
        cursor = conn.cursor()

        try:

            cursor.execute("""
                           SELECT appointments.id,
                                  appointments.patient_id,
                                  appointments.professional_id,
                                  appointments.appointment_date,
                                  appointments.appointment_reason,
                                  appointments.status,
                                  appointments.meeting_link,
                                  appointments.notes,
                                  appointments.created_at,

                                  users.full_name     AS patient_name,
                                  users.profile_photo AS patient_photo

                           FROM appointments

                                    INNER JOIN patients
                                               ON patients.id = appointments.patient_id

                                    INNER JOIN users
                                               ON users.id = patients.user_id

                           WHERE appointments.professional_id = ?

                           ORDER BY appointments.appointment_date ASC

                           """, (
                               professional_id,
                           ))

            appointments = cursor.fetchall()

            return appointments

        finally:

            conn.close()

    # =====================================================
    # RESCHEDULE APPOINTMENT
    # =====================================================

    @staticmethod
    def reschedule(
            appointment_id,
            appointment_date
    ):

        conn = connect()
        cursor = conn.cursor()

        try:

            cursor.execute("""
                           UPDATE appointments

                           SET appointment_date = ?

                           WHERE id = ?

                           """, (

                               appointment_date,

                               appointment_id

                           ))

            conn.commit()

            rows_updated = cursor.rowcount

            return rows_updated

        finally:

            conn.close()


    # =====================================================
    # GET ALL APPOINTMENTS
    # =====================================================

    @staticmethod
    def get_all():

        conn = connect()
        cursor = conn.cursor()

        try:

            cursor.execute("""
                SELECT *

                FROM appointments

                ORDER BY appointment_date DESC

            """)

            appointments = cursor.fetchall()

            return appointments

        finally:

            conn.close()


    # =====================================================
    # UPDATE APPOINTMENT STATUS
    # =====================================================

    @staticmethod
    def update_status(
        appointment_id,
        status
    ):

        conn = connect()
        cursor = conn.cursor()

        try:

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

            return rows_updated

        finally:

            conn.close()


    # =====================================================
    # DELETE APPOINTMENT
    # =====================================================

    @staticmethod
    def delete(appointment_id):

        conn = connect()
        cursor = conn.cursor()

        try:

            cursor.execute("""
                DELETE FROM appointments

                WHERE id = ?

            """, (
                appointment_id,
            ))

            conn.commit()

            rows_deleted = cursor.rowcount

            return rows_deleted

        finally:

            conn.close()


    # =====================================================
    # CHECK EXISTING APPOINTMENT
    # =====================================================

    @staticmethod
    def appointment_exists(
        patient_id,
        professional_id,
        appointment_date
    ):

        conn = connect()
        cursor = conn.cursor()

        try:

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

            return appointment

        finally:

            conn.close()