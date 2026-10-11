from database.bank import connect


class ExamModel:

    @staticmethod
    def create(
        patient_id,
        professional_id,
        exam_name,
        exam_type=None,
        appointment_id=None,
        institution_id=None,
        description=None,
        preparation_instructions=None,
        notes=None,
    ):
        conn = connect()
        try:
            cursor = conn.execute("""
                INSERT INTO exams (
                    patient_id, professional_id, appointment_id, institution_id,
                    exam_name, exam_type, description,
                    preparation_instructions, notes
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                patient_id, professional_id, appointment_id, institution_id,
                exam_name, exam_type, description,
                preparation_instructions, notes
            ))
            conn.commit()
            return cursor.lastrowid
        finally:
            conn.close()

    @staticmethod
    def get_by_id(exam_id):
        conn = connect()
        try:
            return conn.execute("""
                SELECT e.*,
                       p.user_id AS patient_user_id,
                       pu.full_name AS patient_name,
                       pr.user_id AS professional_user_id,
                       pru.full_name AS professional_name,
                       i.name AS institution_name,
                       i.address AS institution_address,
                       i.city AS institution_city,
                       i.state AS institution_state,
                       md.file_name AS result_file_name
                FROM exams e
                INNER JOIN patients p ON p.id = e.patient_id
                INNER JOIN users pu ON pu.id = p.user_id
                INNER JOIN professionals pr ON pr.id = e.professional_id
                INNER JOIN users pru ON pru.id = pr.user_id
                LEFT JOIN institutions i ON i.id = e.institution_id
                LEFT JOIN medical_documents md ON md.id = e.result_document_id
                WHERE e.id = ?
            """, (exam_id,)).fetchone()
        finally:
            conn.close()

    @staticmethod
    def get_by_patient(patient_id):
        conn = connect()
        try:
            return conn.execute("""
                SELECT e.*, pru.full_name AS professional_name,
                       pr.specialty, i.name AS institution_name
                FROM exams e
                INNER JOIN professionals pr ON pr.id = e.professional_id
                INNER JOIN users pru ON pru.id = pr.user_id
                LEFT JOIN institutions i ON i.id = e.institution_id
                WHERE e.patient_id = ?
                ORDER BY e.requested_at DESC, e.id DESC
            """, (patient_id,)).fetchall()
        finally:
            conn.close()

    @staticmethod
    def get_by_professional(professional_id):
        conn = connect()
        try:
            return conn.execute("""
                SELECT e.*, pu.full_name AS patient_name,
                       i.name AS institution_name
                FROM exams e
                INNER JOIN patients p ON p.id = e.patient_id
                INNER JOIN users pu ON pu.id = p.user_id
                LEFT JOIN institutions i ON i.id = e.institution_id
                WHERE e.professional_id = ?
                ORDER BY e.requested_at DESC, e.id DESC
            """, (professional_id,)).fetchall()
        finally:
            conn.close()

    @staticmethod
    def get_all():
        conn = connect()
        try:
            return conn.execute("""
                SELECT e.*, pu.full_name AS patient_name,
                       pru.full_name AS professional_name,
                       i.name AS institution_name
                FROM exams e
                INNER JOIN patients p ON p.id = e.patient_id
                INNER JOIN users pu ON pu.id = p.user_id
                INNER JOIN professionals pr ON pr.id = e.professional_id
                INNER JOIN users pru ON pru.id = pr.user_id
                LEFT JOIN institutions i ON i.id = e.institution_id
                ORDER BY e.requested_at DESC, e.id DESC
            """).fetchall()
        finally:
            conn.close()

    @staticmethod
    def update_status(exam_id, status):
        conn = connect()
        try:
            if status == "completed":
                cursor = conn.execute("""
                    UPDATE exams
                    SET status = ?, completed_at = CURRENT_TIMESTAMP
                    WHERE id = ?
                """, (status, exam_id))
            else:
                cursor = conn.execute("""
                    UPDATE exams SET status = ? WHERE id = ?
                """, (status, exam_id))
            conn.commit()
            return cursor.rowcount
        finally:
            conn.close()

    @staticmethod
    def update_schedule(exam_id, scheduled_at, institution_id=None):
        conn = connect()
        try:
            cursor = conn.execute("""
                UPDATE exams
                SET scheduled_at = ?,
                    institution_id = COALESCE(?, institution_id),
                    status = 'scheduled'
                WHERE id = ?
            """, (scheduled_at, institution_id, exam_id))
            conn.commit()
            return cursor.rowcount
        finally:
            conn.close()

    @staticmethod
    def set_result_document(exam_id, document_id):
        conn = connect()
        try:
            cursor = conn.execute("""
                UPDATE exams SET result_document_id = ? WHERE id = ?
            """, (document_id, exam_id))
            conn.commit()
            return cursor.rowcount
        finally:
            conn.close()

    @staticmethod
    def get_document_patient_id(document_id):
        conn = connect()
        try:
            row = conn.execute(
                "SELECT patient_id FROM medical_documents WHERE id = ?",
                (document_id,)
            ).fetchone()
            return row["patient_id"] if row else None
        finally:
            conn.close()
