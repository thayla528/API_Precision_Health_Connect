from database.bank import connect


class InvitationModel:

    @staticmethod
    # Create invitation
    def create(
        full_name,
        email,
        phone,
        birth_date,
        profile_type,
        interest_reason
    ):
        conn = connect()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO invitations (
                full_name,
                email,
                phone,
                birth_date,
                profile_type,
                interest_reason
            )
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            full_name,
            email,
            phone,
            birth_date,
            profile_type,
            interest_reason
        ))

        conn.commit()

        # Returns the automatically generated ID
        invitation_id = cursor.lastrowid

        conn.close()

        return invitation_id



    @staticmethod
    def mark_as_used(invitation_id):
        conn = connect()
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE invitations
            SET used = 1
            WHERE id = ?
        """, (
            invitation_id,
        ))

        conn.commit()
        conn.close()

    @staticmethod
    def get_by_email(email):

        conn = connect()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT *
            FROM invitations
            WHERE email = ?
        """, (email,))

        invitation = cursor.fetchone()

        conn.close()

        return invitation

    @staticmethod
    def get_by_code(invitation_code):

        conn = connect()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT *
            FROM invitations
            WHERE invitation_code = ?
        """, (invitation_code,))

        invitation = cursor.fetchone()

        conn.close()

        return invitation

    @staticmethod
    def get_by_id(invitation_id):

        conn = connect()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT *
            FROM invitations
            WHERE id = ?
        """, (invitation_id,))

        invitation = cursor.fetchone()

        conn.close()

        return invitation

    @staticmethod
    def get_all():

        conn = connect()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT *
            FROM invitations
            ORDER BY requested_at DESC
        """)

        invitations = cursor.fetchall()

        conn.close()

        return invitations

    @staticmethod
    def approve(invitation_id, invitation_code, administrator_id):

        conn = connect()
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE invitations
            SET
                status = ?,
                invitation_code = ?,
                approved_by = ?,
                approved_at = CURRENT_TIMESTAMP
            WHERE id = ?
        """, (
            "approved",
            invitation_code,
            administrator_id,
            invitation_id
        ))

        conn.commit()
        conn.close()

    @staticmethod
    def reject(invitation_id, administrator_id):

        conn = connect()
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE invitations
            SET
                status = ?,
                approved_by = ?,
                approved_at = CURRENT_TIMESTAMP
            WHERE id = ?
        """, (
            "rejected",
            administrator_id,
            invitation_id
        ))

        conn.commit()
        conn.close()

    @staticmethod
    def get_by_status(status):

        conn = connect()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT *
            FROM invitations
            WHERE status = ?
            ORDER BY requested_at DESC
        """, (status,))

        invitations = cursor.fetchall()

        conn.close()

        return invitations

    @staticmethod
    def delete(invitation_id):

        conn = connect()
        cursor = conn.cursor()

        cursor.execute("""
            DELETE FROM invitations
            WHERE id = ?
        """, (invitation_id,))

        conn.commit()
        conn.close()

    @staticmethod
    def cancel(invitation_id):
        conn = connect()
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE invitations
            SET
                status = ?
            WHERE id = ?
        """, (
            "cancelled",
            invitation_id
        ))

        conn.commit()

        rows_updated = cursor.rowcount

        conn.close()

        return rows_updated