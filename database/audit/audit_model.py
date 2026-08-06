from database.bank import connect


class AuditModel:


    @staticmethod
    def create(
        user_id,
        action,
        table_name,
        record_id,
        old_data,
        new_data
    ):

        conn = connect()

        cursor = conn.cursor()


        cursor.execute("""
            INSERT INTO audit_logs (

                user_id,
                action,
                table_name,
                record_id,
                old_data,
                new_data

            )

            VALUES (?, ?, ?, ?, ?, ?)

        """, (

            user_id,
            action,
            table_name,
            record_id,
            old_data,
            new_data

        ))


        conn.commit()

        conn.close()