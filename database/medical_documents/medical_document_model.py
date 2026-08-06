from database.bank import connect



class MedicalDocumentModel:



    # =====================================================
    # CREATE DOCUMENT
    # =====================================================

    @staticmethod
    def create(
        patient_id,
        uploaded_by,
        file_name,
        document_type,
        file_path
    ):


        conn = connect()

        cursor = conn.cursor()



        cursor.execute("""
            INSERT INTO medical_documents (

                patient_id,

                uploaded_by,

                file_name,

                document_type,

                file_path

            )

            VALUES (?, ?, ?, ?, ?)

        """, (

            patient_id,

            uploaded_by,

            file_name,

            document_type,

            file_path

        ))



        conn.commit()



        document_id = cursor.lastrowid



        conn.close()



        return document_id






    # =====================================================
    # GET BY ID
    # =====================================================

    @staticmethod
    def get_by_id(
            document_id
    ):


        conn = connect()

        cursor = conn.cursor()



        cursor.execute("""
            SELECT *

            FROM medical_documents

            WHERE id = ?

        """, (

            document_id,

        ))



        document = cursor.fetchone()



        conn.close()



        return document






    # =====================================================
    # GET PATIENT DOCUMENTS
    # =====================================================

    @staticmethod
    def get_by_patient(
            patient_id
    ):


        conn = connect()

        cursor = conn.cursor()



        cursor.execute("""
            SELECT *

            FROM medical_documents

            WHERE patient_id = ?

            ORDER BY uploaded_at DESC

        """, (

            patient_id,

        ))



        documents = cursor.fetchall()



        conn.close()



        return documents






    # =====================================================
    # GET DOCUMENTS UPLOADED BY USER
    # =====================================================

    @staticmethod
    def get_by_uploader(
            user_id
    ):


        conn = connect()

        cursor = conn.cursor()



        cursor.execute("""
            SELECT *

            FROM medical_documents

            WHERE uploaded_by = ?

            ORDER BY uploaded_at DESC

        """, (

            user_id,

        ))



        documents = cursor.fetchall()



        conn.close()



        return documents






    # =====================================================
    # GET ALL DOCUMENTS ADMIN
    # =====================================================

    @staticmethod
    def get_all():


        conn = connect()

        cursor = conn.cursor()



        cursor.execute("""
            SELECT *

            FROM medical_documents

            ORDER BY uploaded_at DESC

        """)



        documents = cursor.fetchall()



        conn.close()



        return documents






    # =====================================================
    # DELETE DOCUMENT
    # =====================================================

    @staticmethod
    def delete(
            document_id
    ):


        conn = connect()

        cursor = conn.cursor()



        cursor.execute("""
            DELETE FROM medical_documents

            WHERE id = ?

        """, (

            document_id,

        ))



        conn.commit()



        rows_deleted = cursor.rowcount



        conn.close()



        return rows_deleted