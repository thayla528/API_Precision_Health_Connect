from database.bank import connect


class UserModel:

    @staticmethod
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
            VALUES (?, ?, ?, ?, ?, ?, ?)
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

        user_id = cursor.lastrowid

        conn.close()

        return user_id


    @staticmethod
    def update_password(user_id, hashed_password):
        conn = connect()
        try:
            cursor = conn.cursor()

            cursor.execute("""
                UPDATE users
                SET password = ?
                WHERE id = ?
                AND active = 1
            """, (
                hashed_password,
                user_id
            ))

            conn.commit()
            rows_updated = cursor.rowcount

            return rows_updated

        finally:
            conn.close()


    # =====================================================
    # LISTAR USUÁRIOS ATIVOS
    # =====================================================

    @staticmethod
    def get_active_users():

        conn = connect()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT
                users.id,
                users.full_name,
                users.email,
                administrators.phone AS phone,
                users.role,
                users.profile_type,
                users.active,
                users.profile_photo,
                users.created_at,
                users.last_login

            FROM users

            LEFT JOIN administrators
                ON administrators.user_id = users.id

            WHERE users.active = 1

            ORDER BY users.full_name ASC
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
        """)

        users = cursor.fetchall()

        conn.close()

        return users


    @staticmethod
    def update(
            user_id,
            full_name,
            email,
            password,
            profile_photo
    ):

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
        """, (
            user_id,
        ))

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
        """, (
            user_id,
        ))

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
        """, (
            user_id,
        ))

        conn.commit()

        rows_updated = cursor.rowcount

        conn.close()

        return rows_updated