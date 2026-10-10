from database.bank import connect


class PatientProfessionalModel:

    @staticmethod
    def create(patient_id, professional_id, status="pending"):
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


    # =====================================================
    # GET PATIENTS OF PROFESSIONAL
    # =====================================================



    @staticmethod
    def get_by_professional(professional_id):
        conn = connect()
        cursor = conn.cursor()

        cursor.execute("""
                       SELECT pp.id     AS relationship_id,

                              pp.patient_id,

                              pp.professional_id,

                              pp.status AS relationship_status,

                              pp.created_at,

                              p.user_id,

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

                              p.notes,

                              u.full_name,

                              u.email,

                              u.profile_photo

                       FROM patient_professional pp

                                JOIN patients p
                                     ON pp.patient_id = p.id

                                JOIN users u
                                     ON p.user_id = u.id

                       WHERE pp.professional_id = ?

                         AND pp.status = 'active'

                       ORDER BY pp.created_at DESC

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

    # =====================================================
    # GET PENDING REQUESTS OF PATIENT
    # =====================================================

    @staticmethod
    def get_pending_by_patient(patient_id):

        conn = connect()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT

                pp.id AS relationship_id,

                pp.patient_id,

                pp.professional_id,

                pp.status,

                pp.created_at,

                p.user_id,

                u.full_name,

                u.email,

                u.profile_photo,

                pr.specialty,

                pr.license_number

            FROM patient_professional pp

            JOIN patients p
                ON pp.patient_id = p.id

            JOIN professionals pr
                ON pp.professional_id = pr.id

            JOIN users u
                ON pr.user_id = u.id

            WHERE pp.patient_id = ?

            AND pp.status = 'pending'

            ORDER BY pp.created_at DESC

        """, (patient_id,))

        requests = cursor.fetchall()

        conn.close()

        return requests


    # =====================================================
    # APPROVE RELATIONSHIP
    # =====================================================

    @staticmethod
    def approve(relationship_id):

        conn = connect()
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE patient_professional

            SET status = 'active'

            WHERE id = ?

            AND status = 'pending'

        """, (relationship_id,))

        conn.commit()

        rows_updated = cursor.rowcount

        conn.close()

        return rows_updated


    # =====================================================
    # REJECT RELATIONSHIP
    # =====================================================

    @staticmethod
    def reject(relationship_id):

        conn = connect()
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE patient_professional

            SET status = 'rejected'

            WHERE id = ?

            AND status = 'pending'

        """, (relationship_id,))

        conn.commit()

        rows_updated = cursor.rowcount

        conn.close()

        return rows_updated