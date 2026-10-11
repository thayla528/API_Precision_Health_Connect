from database.bank import connect


class InstitutionModel:

    @staticmethod
    def create(
        name,
        institution_type=None,
        phone=None,
        email=None,
        postal_code=None,
        address=None,
        house_number=None,
        address_line2=None,
        neighborhood=None,
        city=None,
        state=None,
        latitude=None,
        longitude=None,
    ):
        conn = connect()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                INSERT INTO institutions (
                    name, institution_type, phone, email,
                    postal_code, address, house_number, address_line2,
                    neighborhood, city, state, latitude, longitude
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                name, institution_type, phone, email,
                postal_code, address, house_number, address_line2,
                neighborhood, city, state, latitude, longitude
            ))
            conn.commit()
            return cursor.lastrowid
        finally:
            conn.close()

    @staticmethod
    def get_by_id(institution_id):
        conn = connect()
        try:
            return conn.execute(
                "SELECT * FROM institutions WHERE id = ?",
                (institution_id,)
            ).fetchone()
        finally:
            conn.close()

    @staticmethod
    def get_active():
        conn = connect()
        try:
            return conn.execute("""
                SELECT * FROM institutions
                WHERE active = 1
                ORDER BY name COLLATE NOCASE ASC
            """).fetchall()
        finally:
            conn.close()

    @staticmethod
    def get_with_coordinates():
        conn = connect()
        try:
            return conn.execute("""
                SELECT * FROM institutions
                WHERE active = 1
                  AND latitude IS NOT NULL
                  AND longitude IS NOT NULL
                ORDER BY name COLLATE NOCASE ASC
            """).fetchall()
        finally:
            conn.close()

    @staticmethod
    def update(institution_id, fields):
        allowed = {
            "name", "institution_type", "phone", "email", "postal_code",
            "address", "house_number", "address_line2", "neighborhood",
            "city", "state", "latitude", "longitude", "active"
        }
        updates = [(key, value) for key, value in fields.items() if key in allowed]
        if not updates:
            return 0
        assignments = ", ".join(f"{key} = ?" for key, _ in updates)
        values = [value for _, value in updates] + [institution_id]
        conn = connect()
        try:
            cursor = conn.execute(
                f"UPDATE institutions SET {assignments} WHERE id = ?", values
            )
            conn.commit()
            return cursor.rowcount
        finally:
            conn.close()

    @staticmethod
    def link_professional(professional_id, institution_id, is_primary=False):
        conn = connect()
        try:
            if is_primary:
                conn.execute("""
                    UPDATE professional_institutions
                    SET is_primary = 0
                    WHERE professional_id = ?
                """, (professional_id,))

            conn.execute("""
                INSERT INTO professional_institutions (
                    professional_id, institution_id, is_primary, active
                ) VALUES (?, ?, ?, 1)
                ON CONFLICT(professional_id, institution_id)
                DO UPDATE SET active = 1, is_primary = excluded.is_primary
            """, (professional_id, institution_id, int(bool(is_primary))))
            conn.commit()
            return True
        finally:
            conn.close()

    @staticmethod
    def unlink_professional(professional_id, institution_id):
        conn = connect()
        try:
            cursor = conn.execute("""
                UPDATE professional_institutions
                SET active = 0, is_primary = 0
                WHERE professional_id = ? AND institution_id = ?
            """, (professional_id, institution_id))
            conn.commit()
            return cursor.rowcount
        finally:
            conn.close()

    @staticmethod
    def is_professional_linked(professional_id, institution_id):
        conn = connect()
        try:
            return conn.execute("""
                SELECT 1 FROM professional_institutions
                WHERE professional_id = ?
                  AND institution_id = ?
                  AND active = 1
                LIMIT 1
            """, (professional_id, institution_id)).fetchone() is not None
        finally:
            conn.close()

    @staticmethod
    def get_by_professional(professional_id):
        conn = connect()
        try:
            return conn.execute("""
                SELECT i.*, pi.is_primary
                FROM institutions i
                INNER JOIN professional_institutions pi
                    ON pi.institution_id = i.id
                WHERE pi.professional_id = ?
                  AND pi.active = 1
                  AND i.active = 1
                ORDER BY pi.is_primary DESC, i.name COLLATE NOCASE ASC
            """, (professional_id,)).fetchall()
        finally:
            conn.close()
