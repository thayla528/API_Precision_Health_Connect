from database.bank import connect



class RevokedTokenModel:


    @staticmethod
    def add_token(jti):

        conn = connect()

        cursor = conn.cursor()


        cursor.execute("""
            INSERT INTO revoked_tokens (

                jti

            )

            VALUES (?)

        """, (
            jti,
        ))


        conn.commit()

        conn.close()





    @staticmethod
    def is_revoked(jti):

        conn = connect()

        cursor = conn.cursor()


        cursor.execute("""
            SELECT id

            FROM revoked_tokens

            WHERE jti = ?

        """, (
            jti,
        ))


        token = cursor.fetchone()


        conn.close()


        return token is not None