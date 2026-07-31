from database.bank import connect


class PatientProfessional:

    def __init__(
        self,
        id=None,
        patient_id=None,
        professional_id=None,
        status="active",
        created_at=None
    ):
        self.id = id
        self.patient_id = patient_id
        self.professional_id = professional_id
        self.status = status
        self.created_at = created_at


    def save(self):
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
            self.patient_id,
            self.professional_id,
            self.status
        ))

        conn.commit()

        self.id = cursor.lastrowid

        conn.close()

        return self


    @staticmethod
    def get_by_id(id):
        conn = connect()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT *
            FROM patient_professional
            WHERE id = ?
        """, (id,))

        row = cursor.fetchone()

        conn.close()

        if row:
            return PatientProfessional(
                id=row["id"],
                patient_id=row["patient_id"],
                professional_id=row["professional_id"],
                status=row["status"],
                created_at=row["created_at"]
            )

        return None


    @staticmethod
    def get_by_patient(patient_id):
        conn = connect()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT *
            FROM patient_professional
            WHERE patient_id = ?
            AND status = 'active'
        """, (patient_id,))

        rows = cursor.fetchall()

        conn.close()

        return [
            PatientProfessional(
                id=row["id"],
                patient_id=row["patient_id"],
                professional_id=row["professional_id"],
                status=row["status"],
                created_at=row["created_at"]
            )
            for row in rows
        ]


    @staticmethod
    def get_by_professional(professional_id):
        conn = connect()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT *
            FROM patient_professional
            WHERE professional_id = ?
            AND status = 'active'
        """, (professional_id,))

        rows = cursor.fetchall()

        conn.close()

        return [
            PatientProfessional(
                id=row["id"],
                patient_id=row["patient_id"],
                professional_id=row["professional_id"],
                status=row["status"],
                created_at=row["created_at"]
            )
            for row in rows
        ]


    def deactivate(self):
        conn = connect()
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE patient_professional
            SET status = 'inactive'
            WHERE id = ?
        """, (self.id,))

        conn.commit()

        conn.close()