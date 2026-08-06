from database.bank import connect


class PatientProfessionalModel:

    @staticmethod
    def create(patient_id, professional_id, status="active"):
        conn = connect()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO patient_professional (
                patient_id,
                professional_id,
                status
            )
            VALUES (?, ?, ?)
        """, (
            patient_id,
            professional_id,
            status
        ))

        conn.commit()

        relationship_id = cursor.lastrowid

        conn.close()

        return relationship_id

    @staticmethod
    def get_by_id(relationship_id):
        conn = connect()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT *
            FROM patient_professional
            WHERE id = ?
        """, (relationship_id,))

        relationship = cursor.fetchone()

        conn.close()

        return relationship

    @staticmethod
    def get_by_patient(patient_id):
        conn = connect()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT *
            FROM patient_professional
            WHERE patient_id = ?
            AND status = 'active'
            ORDER BY created_at DESC
        """, (patient_id,))

        relationships = cursor.fetchall()

        conn.close()

        return relationships

    @staticmethod
    def get_by_professional(professional_id):
        conn = connect()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT *
            FROM patient_professional
            WHERE professional_id = ?
            AND status = 'active'
            ORDER BY created_at DESC
        """, (professional_id,))

        relationships = cursor.fetchall()

        conn.close()

        return relationships

    @staticmethod
    def relationship_exists(patient_id, professional_id):
        conn = connect()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT *
            FROM patient_professional
            WHERE patient_id = ?
            AND professional_id = ?
            AND status = 'active'
        """, (
            patient_id,
            professional_id
        ))

        relationship = cursor.fetchone()

        conn.close()

        return relationship

    @staticmethod
    def deactivate(relationship_id):
        conn = connect()
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE patient_professional
            SET status = 'inactive'
            WHERE id = ?
            AND status = 'active'
        """, (relationship_id,))

        conn.commit()

        rows_updated = cursor.rowcount

        conn.close()

        return rows_updated

    @staticmethod
    def get_all():
        conn = connect()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT *
            FROM patient_professional
            ORDER BY created_at DESC
        """)

        relationships = cursor.fetchall()

        conn.close()

        return relationships