from database.bank import connect

class UserModel:
    @staticmethod
    # Create invitation
    def create(
            invitation_id,
            full_name,
            email,
            password,
            profile_type,
            profile_photo

    ):
        conn = connect()
        cursor = conn.cursor()

        cursor.execute("""
                INSERT INTO users (
                    invitation_id,
                    full_name,
                    email,
                    password,
                    role,
                    profile_type,
                    profile_photo
                    
                    
                )
                VALUES ( ?, ?, ?, ?, ?, ?,?)
            """, (
            invitation_id,
            full_name,
            email,
            password,
            profile_type,
            profile_type,
            profile_photo


        ))

        conn.commit()

        # Returns the automatically generated ID
        user_id = cursor.lastrowid

        conn.close()

        return user_id

    @staticmethod
    def get_active_users():
        conn = connect()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT *
            FROM users
            WHERE active = 1
            ORDER BY full_name ASC
        """)

        users = cursor.fetchall()

        conn.close()

        return users

    @staticmethod
    def get_by_email(email):
        conn = connect()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT *
            FROM users
            WHERE email = ?
            AND active = 1
        """, (
            email,
        ))

        user = cursor.fetchone()

        conn.close()

        return user

    @staticmethod
    def get_by_id(user_id):
        conn = connect()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT *
            FROM users
            WHERE id = ?
            AND active = 1
        """, (
            user_id,
        ))

        user = cursor.fetchone()

        conn.close()

        return user

    @staticmethod
    def get_all():
        conn = connect()
        cursor = conn.cursor()

        cursor.execute("""

                    SELECT *
                    FROM users
                     ORDER BY full_name ASC
                     
                   
                """, ())

        users = cursor.fetchall()
        # coloca em ordem alfabética  ORDER BY full_name ASC
        conn.close()

        return users

    @staticmethod
    def update(user_id, full_name, email, password, profile_photo):
        conn = connect()
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE users
            SET
                full_name = ?,
                email = ?,
                password = ?,
                profile_photo = ?
            WHERE id = ?
        """, (
            full_name,
            email,
            password,
            profile_photo,
            user_id
        ))

        conn.commit()

        rows_updated = cursor.rowcount

        conn.close()

        return rows_updated

    @staticmethod
    def deactivate(user_id):
        conn = connect()
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE users
            SET active = 0
            WHERE id = ?
        """, (user_id,))

        conn.commit()

        rows_updated = cursor.rowcount

        conn.close()

        return rows_updated

    @staticmethod
    def activate(user_id):
        conn = connect()
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE users
            SET active = 1
            WHERE id = ?
        """, (user_id,))

        conn.commit()

        rows_updated = cursor.rowcount

        conn.close()

        return rows_updated

    @staticmethod
    def update_last_login(user_id):
        conn = connect()
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE users
            SET last_login = CURRENT_TIMESTAMP
            WHERE id = ?
        """, (user_id,))

        conn.commit()

        rows_updated = cursor.rowcount

        conn.close()

        return rows_updated

    #    SELECT → busca dados → usa fetchone() / fetchall()
    #    INSERT → cria dados → usa lastrowid
    #    UPDATE → altera dados → usa commit() e pode usar rowcount
    #    DELETE → remove dados → usa commit()







