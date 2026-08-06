import json

from database.audit.audit_model import AuditModel



class AuditService:


    def __init__(self):

        self.model = AuditModel()



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