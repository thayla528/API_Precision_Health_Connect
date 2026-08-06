from datetime import datetime

from database.patients.patient_model import PatientModel



class PatientService:


    def get_dashboard(self, user_id):


        user = PatientModel.get_user(
            user_id
        )


        next_appointment = PatientModel.get_next_appointment(
            user_id
        )


        recent_appointments = PatientModel.get_recent_appointments(
            user_id
        )


        upcoming_appointments = PatientModel.get_upcoming_appointments(
            user_id
        )


        medical_documents = PatientModel.get_documents(
            user_id
        )


        notifications = PatientModel.get_notifications(
            user_id
        )


        return {

            "user": user,


            "current_date":
                datetime.now().strftime(
                    "%d/%m/%Y"
                ),


            "next_appointment":
                next_appointment,


            "pending_exams": 0,


            "unread_messages":
                PatientModel.count_messages(
                    user_id
                ),


            "unread_notifications":
                PatientModel.count_notifications(
                    user_id
                ),


            "recent_appointments":
                recent_appointments,


            "upcoming_appointments":
                upcoming_appointments,


            "medical_documents":
                medical_documents,


            "notifications":
                notifications,


            "timeline":
                PatientModel.get_timeline(user_id),


            "health_summary": {
            "consultations": 0,
            "exams": 0,
            "medications": 0,
            "vaccines": 0
        },

        }
    def get_profile(self, user_id):


        profile = PatientModel.get_profile(
            user_id
        )


        return profile