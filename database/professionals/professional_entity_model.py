from database.bank import connect


class ProfessionalEntityModel:

    @staticmethod
    def create(user_id):
        conn = connect()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO professionals (
                user_id,
                specialty,
                license_number
            )
            VALUES (?, ?, ?)
        """, (
            user_id,
            "Não informado",
            "TEMP-" + str(user_id)
        ))

        conn.commit()

        professional_id = cursor.lastrowid

        conn.close()

        return professional_id


    @staticmethod
    def get_by_id(professional_id):

        conn = connect()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT *
            FROM professionals
            WHERE id = ?
        """, (professional_id,))

        professional = cursor.fetchone()

        conn.close()

        return professional



    @staticmethod
    def get_by_user_id(user_id):

        conn = connect()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT *
            FROM professionals
            WHERE user_id = ?
        """, (user_id,))

        professional = cursor.fetchone()

        conn.close()

        return professional