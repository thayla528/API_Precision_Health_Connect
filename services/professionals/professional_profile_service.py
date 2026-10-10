
from database.professionals.professional_model import ProfessionalModel

from werkzeug.security import generate_password_hash


class ProfessionalProfileService:

    def __init__(self):

        self.professional_model = ProfessionalModel()


    # =====================================================
    # CREATE PROFESSIONAL PROFILE
    # =====================================================

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

            "message":
                "Professional profile created successfully.",

            "professional_id":
                professional_id

        }


    # =====================================================
    # GET PROFESSIONAL PROFILE
    # =====================================================

    def get_profile(self, user_id):

        profile = self.professional_model.get_profile(
            user_id
        )


        if not profile:

            return {

                "success": False,

                "message":
                    "Professional profile not found."

            }


        return {

            "success": True,

            "professional": {

                "id":
                    profile["professional_id"],

                "user_id":
                    profile["user_id"],

                "full_name":
                    profile["full_name"],

                "email":
                    profile["email"],

                "role":
                    profile["role"],

                "profile_type":
                    profile["profile_type"],

                "profile_photo":
                    profile["profile_photo"],

                "active":
                    profile["user_active"],

                "last_login":
                    profile["last_login"],

                "created_at":
                    profile["professional_created_at"],

                "specialty":
                    profile["specialty"],

                "license_number":
                    profile["license_number"],

                "institution":
                    profile["institution"],

                "practice_area":
                    profile["practice_area"],

                "phone":
                    profile["phone"],

                "professional_email":
                    profile["professional_email"]

            }

        }


    # =====================================================
    # UPDATE PROFESSIONAL PROFILE
    # =====================================================

    def update_profile(

            self,

            user_id,

            full_name=None,

            email=None,

            password=None,

            profile_photo=None,

            specialty=None,

            license_number=None,

            institution=None,

            practice_area=None,

            phone=None,

            professional_email=None

    ):

        existing = self.professional_model.get_profile(
            user_id
        )


        if not existing:

            return {

                "success": False,

                "message":
                    "Professional profile not found."

            }


        # =================================================
        # HASH DA SENHA
        # =================================================

        hashed_password = None


        if password:

            hashed_password = generate_password_hash(
                password
            )


        # =================================================
        # ATUALIZAR USERS
        # =================================================

        self.professional_model.update_user(

            user_id=user_id,

            full_name=full_name,

            email=email,

            password=hashed_password,

            profile_photo=profile_photo

        )


        # =================================================
        # ATUALIZAR PROFESSIONALS
        # =================================================

        self.professional_model.update_profile(

            user_id=user_id,

            specialty=specialty,

            license_number=license_number,

            institution=institution,

            practice_area=practice_area,

            phone=phone,

            professional_email=professional_email

        )


        # =================================================
        # BUSCAR PERFIL ATUALIZADO
        # =================================================

        updated = self.professional_model.get_profile(
            user_id
        )


        return {

            "success": True,

            "message":
                "Professional profile updated successfully.",

            "professional": updated

        }

