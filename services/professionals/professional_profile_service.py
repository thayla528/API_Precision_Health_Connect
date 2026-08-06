from database.professionals.professional_model import ProfessionalModel


class ProfessionalProfileService:


    def __init__(self):

        self.professional_model = ProfessionalModel()



    def create_profile(
            self,
            user_id,
            specialty,
            license_number,
            institution=None,
            practice_area=None,
            phone=None,
            professional_email=None
    ):


        existing = self.professional_model.get_profile(
            user_id
        )


        if existing:

            return {
                "success": False,
                "message": "Professional profile already exists."
            }



        professional_id = self.professional_model.create(
            user_id,
            specialty,
            license_number,
            institution,
            practice_area,
            phone,
            professional_email
        )


        return {
            "success": True,
            "message": "Professional profile created successfully.",
            "professional_id": professional_id
        }