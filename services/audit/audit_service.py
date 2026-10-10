import json

from database.audit.audit_model import AuditModel


class AuditService:

    def __init__(self):

        self.model = AuditModel()


    # =====================================================
    # REGISTRAR LOG
    # =====================================================

    def register(
        self,
        user_id,
        action,
        table_name,
        record_id,
        old_data,
        new_data
    ):

        self.model.create(

            user_id,

            action,

            table_name,

            record_id,

            json.dumps(old_data),

            json.dumps(new_data)

        )


    # =====================================================
    # LISTAR LOGS
    # =====================================================

    def get_logs(
        self,
        search=None,
        action=None,
        page=1,
        per_page=10
    ):

        result = self.model.get_logs(

            search=search,

            action=action,

            page=page,

            per_page=per_page

        )


        logs = []


        for log in result["logs"]:

            old_data = self._parse_json(
                log["old_data"]
            )

            new_data = self._parse_json(
                log["new_data"]
            )


            # =================================================
            # ADMINISTRADOR QUE EXECUTOU A AÇÃO
            # =================================================

            administrator = {

                "name":
                    log["administrator_name"],

                "email":
                    log["administrator_email"]

            }


            # =================================================
            # USUÁRIO AFETADO
            # =================================================

            affected_user = None


            # -------------------------------------------------
            # CASO 1:
            # O registro afetado está em USERS
            # -------------------------------------------------

            if log["affected_user_name"]:

                affected_user = {

                    "name":
                        log["affected_user_name"],

                    "email":
                        log["affected_user_email"]

                }


            # -------------------------------------------------
            # CASO 2:
            # O registro afetado está em INVITATIONS
            #
            # Exemplo:
            # CREATE_ADMINISTRATOR
            # -------------------------------------------------

            elif log["invitation_name"]:

                affected_user = {

                    "name":
                        log["invitation_name"],

                    "email":
                        log["invitation_email"],

                    "profile_type":
                        log["invitation_profile_type"],

                    "status":
                        log["invitation_status"]

                }


            # =================================================
            # CONVITE
            # =================================================

            invitation = None


            if log["invitation_name"]:

                invitation = {

                    "name":
                        log["invitation_name"],

                    "email":
                        log["invitation_email"],

                    "profile_type":
                        log["invitation_profile_type"],

                    "status":
                        log["invitation_status"]

                }


            # =================================================
            # RESULTADO
            # =================================================

            result_status = None


            if isinstance(new_data, dict):

                result_status = new_data.get(
                    "status"
                )


            if not result_status and isinstance(old_data, dict):

                result_status = old_data.get(
                    "status"
                )


            # =================================================
            # LOG FINAL
            # =================================================

            logs.append({

                "id":
                    log["id"],

                "user_id":
                    log["user_id"],

                "action":
                    log["action"],

                "table_name":
                    log["table_name"],

                "record_id":
                    log["record_id"],

                "old_data":
                    old_data,

                "new_data":
                    new_data,

                "created_at":
                    log["created_at"],

                "administrator":
                    administrator,

                "affected_user":
                    affected_user,

                "invitation":
                    invitation,

                "result":
                    result_status,

                "details":
                    new_data

            })


        return {

            "logs":
                logs,

            "total":
                result["total"],

            "page":
                result["page"],

            "per_page":
                result["per_page"],

            "total_pages":
                result["total_pages"]

        }


    # =====================================================
    # CONVERTER JSON
    # =====================================================

    @staticmethod
    def _parse_json(data):

        if not data:

            return None


        try:

            return json.loads(data)

        except (
            json.JSONDecodeError,
            TypeError
        ):

            return data