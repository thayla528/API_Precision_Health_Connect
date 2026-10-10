from database.bank import connect


class AuditModel:

    # =====================================================
    # CRIAR LOG DE AUDITORIA
    # =====================================================

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


    # =====================================================
    # LISTAR LOGS DE AUDITORIA
    # =====================================================

    @staticmethod
    def get_logs(
        search=None,
        action=None,
        page=1,
        per_page=10
    ):

        conn = connect()
        cursor = conn.cursor()

        # =================================================
        # CONDIÇÕES
        # =================================================

        conditions = []
        parameters = []

        # =================================================
        # BUSCA
        # =================================================

        if search:

            search_value = f"%{search.strip()}%"

            conditions.append("""
                (
                    administrator.full_name LIKE ?
                    OR administrator.email LIKE ?

                    OR affected_user.full_name LIKE ?
                    OR affected_user.email LIKE ?

                    OR affected_invitation.full_name LIKE ?
                    OR affected_invitation.email LIKE ?

                    OR audit_logs.action LIKE ?
                    OR audit_logs.table_name LIKE ?
                )
            """)

            parameters.extend([
                search_value,
                search_value,
                search_value,
                search_value,
                search_value,
                search_value,
                search_value,
                search_value
            ])

        # =================================================
        # FILTRO POR AÇÃO
        # =================================================

        if action:

            conditions.append("""
                audit_logs.action = ?
            """)

            parameters.append(action)

        # =================================================
        # WHERE
        # =================================================

        where_clause = ""

        if conditions:

            where_clause = (
                "WHERE " +
                " AND ".join(conditions)
            )

        # =================================================
        # CONTAR RESULTADOS
        # =================================================

        cursor.execute(f"""
            SELECT COUNT(*)

            FROM audit_logs

            INNER JOIN users AS administrator
                ON administrator.id = audit_logs.user_id

            LEFT JOIN users AS affected_user
                ON audit_logs.table_name = 'users'
                AND affected_user.id = audit_logs.record_id

            LEFT JOIN invitations AS affected_invitation
                ON audit_logs.table_name = 'invitations'
                AND affected_invitation.id = audit_logs.record_id

            {where_clause}

        """, parameters)

        total = cursor.fetchone()[0]

        # =================================================
        # PAGINAÇÃO
        # =================================================

        offset = (page - 1) * per_page

        # =================================================
        # BUSCAR LOGS
        # =================================================

        cursor.execute(f"""
            SELECT

                audit_logs.id,
                audit_logs.user_id,
                audit_logs.action,
                audit_logs.table_name,
                audit_logs.record_id,
                audit_logs.old_data,
                audit_logs.new_data,
                audit_logs.created_at,

                -- =========================================
                -- ADMINISTRADOR
                -- =========================================

                administrator.full_name
                    AS administrator_name,

                administrator.email
                    AS administrator_email,

                -- =========================================
                -- USUÁRIO AFETADO
                -- =========================================

                affected_user.full_name
                    AS affected_user_name,

                affected_user.email
                    AS affected_user_email,

                -- =========================================
                -- CONVITE AFETADO
                -- =========================================

                affected_invitation.full_name
                    AS invitation_name,

                affected_invitation.email
                    AS invitation_email,

                affected_invitation.profile_type
                    AS invitation_profile_type,

                affected_invitation.status
                    AS invitation_status

            FROM audit_logs

            -- =============================================
            -- ADMINISTRADOR QUE EXECUTOU A AÇÃO
            -- =============================================

            INNER JOIN users AS administrator
                ON administrator.id = audit_logs.user_id

            -- =============================================
            -- USUÁRIO AFETADO
            -- =============================================

            LEFT JOIN users AS affected_user
                ON audit_logs.table_name = 'users'
                AND affected_user.id = audit_logs.record_id

            -- =============================================
            -- CONVITE AFETADO
            -- =============================================

            LEFT JOIN invitations AS affected_invitation
                ON audit_logs.table_name = 'invitations'
                AND affected_invitation.id = audit_logs.record_id

            {where_clause}

            ORDER BY audit_logs.created_at DESC

            LIMIT ? OFFSET ?

        """, parameters + [
            per_page,
            offset
        ])

        logs = cursor.fetchall()

        conn.close()

        # =================================================
        # TOTAL DE PÁGINAS
        # =================================================

        total_pages = (
            (total + per_page - 1) // per_page
            if total > 0
            else 0
        )

        # =================================================
        # RETORNO
        # =================================================

        return {

            "logs": logs,

            "total": total,

            "page": page,

            "per_page": per_page,

            "total_pages": total_pages

        }