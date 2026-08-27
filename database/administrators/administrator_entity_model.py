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

    @staticmethod
    def get_all(
        search=None,
        status=None,
        page=1,
        per_page=10
    ):

        conn = connect()
        cursor = conn.cursor()

        conditions = []
        parameters = []

        if search:
            conditions.append("""
                (
                    users.full_name LIKE ?
                    OR users.email LIKE ?
                )
            """)

            search_value = f"%{search}%"

            parameters.extend([
                search_value,
                search_value
            ])

        if status in ["ativo", "inativo"]:
            conditions.append("""
                users.active = ?
            """)

            if status == "ativo":
                parameters.append(1)
            else:
                parameters.append(0)

        where_clause = ""

        if conditions:
            where_clause = "WHERE " + " AND ".join(conditions)

        cursor.execute(f"""
            SELECT COUNT(*)
            FROM administrators
            INNER JOIN users
                ON users.id = administrators.user_id
            {where_clause}
        """, parameters)

        total = cursor.fetchone()[0]

        offset = (page - 1) * per_page


        cursor.execute(f"""
            SELECT
                administrators.id,
                administrators.user_id,
                users.full_name,
                users.email,
                invitations.phone,
                users.role,
                users.profile_type,
                users.profile_photo,
                users.active,
                users.created_at,
                users.last_login
            FROM administrators
            INNER JOIN users
                ON users.id = administrators.user_id
            LEFT JOIN invitations
                ON invitations.id = users.invitation_id
            {where_clause}
            ORDER BY users.full_name ASC
            LIMIT ? OFFSET ?
        """, parameters + [per_page, offset])

        administrators = cursor.fetchall()

        conn.close()

        total_pages = (
            (total + per_page - 1) // per_page
            if total > 0
            else 0
        )

        return {
            "administrators": administrators,
            "total": total,
            "page": page,
            "per_page": per_page,
            "total_pages": total_pages
        }



    @staticmethod
    def get_details(administrator_id):

        conn = connect()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT
                administrators.id,
                administrators.user_id,
                users.full_name,
                users.email,
                users.phone,
                users.role,
                users.profile_type,
                users.profile_photo,
                users.active,
                users.created_at,
                users.last_login,
                users.invitation_id
            FROM administrators
            INNER JOIN users
                ON users.id = administrators.user_id
            WHERE administrators.id = ?
        """, (administrator_id,))

        row = cursor.fetchone()

        conn.close()

        if not row:
            return None

        if isinstance(row, dict) or (
                hasattr(row, "keys") and
                callable(getattr(row, "keys"))
        ):
            return dict(row)

        return {
            "id": row[0],
            "user_id": row[1],
            "full_name": row[2],
            "email": row[3],
            "phone": row[4],
            "role": row[5],
            "profile_type": row[6],
            "profile_photo": row[7],
            "active": row[8],
            "created_at": row[9],
            "last_login": row[10],
            "invitation_id": row[11]
        }

    @staticmethod
    def get_user_by_id(user_id):

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