from database.bank import connect


class AdministratorEntityModel:


    @staticmethod
    def create(user_id):

        conn = connect()
        cursor = conn.cursor()


        cursor.execute("""
            INSERT INTO administrators (
                user_id
            )
            VALUES (?)
        """, (
            user_id,
        ))


        conn.commit()


        administrator_id = cursor.lastrowid


        conn.close()


        return administrator_id



    @staticmethod
    def get_by_id(administrator_id):

        conn = connect()
        cursor = conn.cursor()


        cursor.execute("""
            SELECT *
            FROM administrators
            WHERE id = ?
        """, (
            administrator_id,
        ))


        administrator = cursor.fetchone()


        conn.close()


        return administrator



    @staticmethod
    def get_by_user_id(user_id):

        conn = connect()
        cursor = conn.cursor()


        cursor.execute("""
            SELECT *
            FROM administrators
            WHERE user_id = ?
        """, (
            user_id,
        ))


        administrator = cursor.fetchone()


        conn.close()


        return administrator