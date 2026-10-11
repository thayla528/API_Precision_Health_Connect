from database.exams.exam_model import ExamModel
from database.institutions.institution_model import InstitutionModel
from database.appointments.appointment_model import AppointmentModel
from database.patients.patient_entity_model import PatientEntityModel
from database.professionals.professional_entity_model import ProfessionalEntityModel
from database.patients.patient_professional_model import PatientProfessionalModel


class ExamService:
    ALLOWED_STATUS = {"requested", "scheduled", "in_progress", "completed", "cancelled"}

    def __init__(self):
        self.exam_model = ExamModel()
        self.institution_model = InstitutionModel()
        self.appointment_model = AppointmentModel()
        self.patient_model = PatientEntityModel()
        self.professional_model = ProfessionalEntityModel()
        self.relationship_model = PatientProfessionalModel()

    def create_exam(self, professional_user_id, patient_id, data):
        professional = self.professional_model.get_by_user_id(professional_user_id)
        if not professional:
            return {"success": False, "message": "Professional profile not found."}
        patient = self.patient_model.get_by_id(patient_id)
        if not patient:
            return {"success": False, "message": "Patient not found."}
        relationship = self.relationship_model.relationship_exists(patient_id, professional["id"])
        if not relationship:
            return {"success": False, "message": "Patient is not linked to this professional."}

        exam_name = (data.get("exam_name") or "").strip()
        if not exam_name:
            return {"success": False, "message": "exam_name is required."}

        appointment_id = data.get("appointment_id")
        if appointment_id is not None:
            appointment = self.appointment_model.get_by_id(appointment_id)
            if not appointment:
                return {"success": False, "message": "Appointment not found."}
            if appointment["patient_id"] != patient_id or appointment["professional_id"] != professional["id"]:
                return {"success": False, "message": "Appointment does not belong to this patient and professional."}
            if appointment["status"] == "cancelled":
                return {"success": False, "message": "Cannot request an exam for a cancelled appointment."}

        institution_id = data.get("institution_id")
        if institution_id is not None:
            institution = self.institution_model.get_by_id(institution_id)
            if not institution or not institution["active"]:
                return {"success": False, "message": "Active institution not found."}
            if not self.institution_model.is_professional_linked(professional["id"], institution_id):
                return {"success": False, "message": "Professional is not linked to this institution."}

        exam_id = self.exam_model.create(
            patient_id=patient_id,
            professional_id=professional["id"],
            exam_name=exam_name,
            exam_type=data.get("exam_type"),
            appointment_id=appointment_id,
            institution_id=institution_id,
            description=data.get("description"),
            preparation_instructions=data.get("preparation_instructions"),
            notes=data.get("notes"),
        )
        return {"success": True, "message": "Exam requested successfully.", "exam_id": exam_id}

    def get_exam(self, exam_id):
        exam = self.exam_model.get_by_id(exam_id)
        if not exam:
            return None
        return dict(exam)

    def get_patient_exams(self, patient_id):
        return {"success": True, "exams": [dict(row) for row in self.exam_model.get_by_patient(patient_id)]}

    def get_professional_exams(self, professional_id):
        return {"success": True, "exams": [dict(row) for row in self.exam_model.get_by_professional(professional_id)]}

    def get_all_exams(self):
        return {"success": True, "exams": [dict(row) for row in self.exam_model.get_all()]}

    def update_status(self, exam_id, status):
        if status not in self.ALLOWED_STATUS:
            return {"success": False, "message": "Invalid exam status."}
        exam = self.exam_model.get_by_id(exam_id)
        if not exam:
            return {"success": False, "message": "Exam not found."}
        if exam["status"] in ("completed", "cancelled"):
            return {"success": False, "message": "This exam can no longer change status."}
        if status == "completed" and not exam["result_document_id"]:
            return {"success": False, "message": "Attach the result document before marking the exam completed."}
        if self.exam_model.update_status(exam_id, status) == 0:
            return {"success": False, "message": "Exam status was not updated."}
        return {"success": True, "message": "Exam status updated successfully."}

    def schedule_exam(self, exam_id, scheduled_at, institution_id=None):
        if not scheduled_at:
            return {"success": False, "message": "scheduled_at is required."}
        exam = self.exam_model.get_by_id(exam_id)
        if not exam:
            return {"success": False, "message": "Exam not found."}
        if exam["status"] in ("completed", "cancelled"):
            return {"success": False, "message": "This exam cannot be scheduled."}
        if institution_id is not None:
            institution = self.institution_model.get_by_id(institution_id)
            if not institution or not institution["active"]:
                return {"success": False, "message": "Active institution not found."}
            if not self.institution_model.is_professional_linked(exam["professional_id"], institution_id):
                return {"success": False, "message": "Professional is not linked to this institution."}
        updated = self.exam_model.update_schedule(exam_id, scheduled_at, institution_id)
        if not updated:
            return {"success": False, "message": "Exam was not scheduled."}
        return {"success": True, "message": "Exam scheduled successfully."}

    def attach_result_document(self, exam_id, document_id):
        exam = self.exam_model.get_by_id(exam_id)
        if not exam:
            return {"success": False, "message": "Exam not found."}
        document_patient_id = self.exam_model.get_document_patient_id(document_id)
        if document_patient_id is None:
            return {"success": False, "message": "Medical document not found."}
        if document_patient_id != exam["patient_id"]:
            return {"success": False, "message": "Result document must belong to the same patient as the exam."}
        if exam["status"] == "cancelled":
            return {"success": False, "message": "Cannot attach a result to a cancelled exam."}
        self.exam_model.set_result_document(exam_id, document_id)
        return {"success": True, "message": "Exam result document attached successfully."}
