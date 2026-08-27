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
            profile_photo,
            phone=None
    ):
        conn = connect()
        cursor = conn.cursor()

        # Correção da query e da tupla para bater exatamente 7 colunas com 7 valores
        cursor.execute("""
                INSERT INTO users (
                    invitation_id,
                    full_name,
                    email,
                    password,
                    role,
                    profile_type,
                    profile_photo,
                    phone
                    
                )
                VALUES (?, ?, ?, ?, ?, ?, ?,?)
            """, (
                invitation_id,
                full_name,
                email,
                password,
                profile_type,  # Mapeia para a coluna role
                profile_type,  # Mapeia para a coluna profile_type
                profile_photo  # Mapeia para a coluna profile_photo
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
        conn.close()

        return users

    @staticmethod
    def update(user_id, full_name, email, password, profile_photo, phone=None):
        conn = connect()
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE users
            SET
                full_name = ?,
                email = ?,
                password = ?,
                profile_photo = ?,
                phone = ?
            WHERE id = ?
        """, (
            full_name,
            email,
            password,
            profile_photo,
            phone,
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

    @staticmethod
    def get_by_id_any_status(user_id):
        conn = connect()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT *
            FROM users
            WHERE id = ?
        """, (
            user_id,
        ))

        user = cursor.fetchone()

        conn.close()

        return user
