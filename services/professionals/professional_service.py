from database.professionals.professional_model import ProfessionalModel


class ProfessionalService:

    def __init__(self):
        self.professional_model = ProfessionalModel()


    def get_user(self, user_id):

        user = self.professional_model.get_user(user_id)

        if not user:
            return {
                "success": False,
                "message": "User not found."
            }

        return {
            "success": True,
            "user": user
        }


    def get_profile(self, user_id):

        profile = self.professional_model.get_profile(user_id)

        if not profile:
            return {
                "success": False,
                "message": "Profile not found."
            }

        return {
            "success": True,
            "profile": profile
        }


    def get_next_appointment(self, user_id):

        appointment = self.professional_model.get_next_appointment(
            user_id
        )

        return {
            "success": True,
            "appointment": appointment
        }


    def get_recent_appointments(self, user_id):

        appointments = (
            self.professional_model
            .get_recent_appointments(user_id)
        )

        return {
            "success": True,
            "appointments": appointments
        }


    def get_upcoming_appointments(self, user_id):

        appointments = (
            self.professional_model
            .get_upcoming_appointments(user_id)
        )

        return {
            "success": True,
            "appointments": appointments
        }


    def count_messages(self, user_id):

        total = self.professional_model.count_messages(user_id)

        return {
            "success": True,
            "total": total
        }


    def count_notifications(self, user_id):

        total = self.professional_model.count_notifications(user_id)

        return {
            "success": True,
            "total": total
        }