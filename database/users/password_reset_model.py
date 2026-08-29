
from database.bank import connect


class PasswordResetModel:

    # =====================================================
    # CRIAR CÓDIGO DE RECUPERAÇÃO
    # =====================================================

    @staticmethod
    def create(
        user_id,
        email,
        reset_code,
        expires_at
    ):

        conn = connect()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO password_resets (
                user_id,
                email,
                reset_code,
                expires_at
            )
            VALUES (?, ?, ?, ?)
        """, (
            user_id,
            email,
            reset_code,
            expires_at
        ))

        conn.commit()

        reset_id = cursor.lastrowid

        conn.close()

        return reset_id


    # =====================================================
    # BUSCAR CÓDIGO
    # =====================================================

    @staticmethod
    def get_by_code(reset_code):

        conn = connect()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT *
            FROM password_resets
            WHERE reset_code = ?
            ORDER BY created_at DESC
            LIMIT 1
        """, (
            reset_code,
        ))

        reset = cursor.fetchone()

        conn.close()

        return reset


    # =====================================================
    # MARCAR CÓDIGO COMO UTILIZADO
    # =====================================================

    @staticmethod
    def mark_as_used(reset_id):

        conn = connect()
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE password_resets
            SET used = 1
            WHERE id = ?
        """, (
            reset_id,
        ))

        conn.commit()

        rows_updated = cursor.rowcount

        conn.close()

        return rows_updated

