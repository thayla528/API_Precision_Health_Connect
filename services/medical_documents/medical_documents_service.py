from database.medical_documents.medical_document_model import MedicalDocumentModel

from database.patients.patient_entity_model import PatientEntityModel

from database.professionals.professional_entity_model import ProfessionalEntityModel

from database.patients.patient_professional_model import PatientProfessionalModel



class MedicalDocumentService:



    def __init__(self):

        self.document_model = MedicalDocumentModel()

        self.patient_model = PatientEntityModel()

        self.professional_model = ProfessionalEntityModel()

        self.relationship_model = PatientProfessionalModel()





    # =====================================================
    # UPLOAD DOCUMENT
    # =====================================================

    def upload_document(
            self,
            uploaded_by,
            patient_id,
            file_name,
            document_type,
            saved_path
    ):


        patient = (
            self.patient_model
            .get_by_id(
                patient_id
            )
        )


        if not patient:

            return {

                "success": False,

                "message": "Patient not found."

            }





        professional = (
            self.professional_model
            .get_by_user_id(
                uploaded_by
            )
        )


        if professional:


            relationship = (
                self.relationship_model
                .relationship_exists(

                    patient_id,

                    professional["id"]

                )
            )


            if not relationship:

                return {

                    "success": False,

                    "message": "Professional is not linked to this patient."

                }

        document_id = (
            self.document_model
            .create(

                patient_id,

                uploaded_by,

                file_name,

                document_type,

                saved_path

            )
        )




        return {

            "success": True,

            "message": "Document uploaded successfully.",

            "document_id": document_id

        }





    # =====================================================
    # GET PATIENT DOCUMENTS
    # =====================================================

    def get_patient_documents(
            self,
            patient_id
    ):


        documents = (
            self.document_model
            .get_by_patient(

                patient_id

            )
        )



        return {

            "success": True,

            "documents": [

                dict(document)

                for document in documents

            ]

        }





    # =====================================================
    # GET ALL DOCUMENTS ADMIN
    # =====================================================

    def get_all_documents(
            self
    ):


        documents = (
            self.document_model
            .get_all()
        )


        return {

            "success": True,

            "documents": [

                dict(document)

                for document in documents

            ]

        }





    # =====================================================
    # GET DOCUMENT BY ID
    # =====================================================

    def get_document(
            self,
            document_id
    ):


        document = (
            self.document_model
            .get_by_id(

                document_id

            )
        )


        if not document:

            return {

                "success": False,

                "message": "Document not found."

            }



        return {

            "success": True,

            "document": dict(document)

        }





    # =====================================================
    # DELETE DOCUMENT
    # =====================================================

    def delete_document(
            self,
            document_id
    ):


        document = (
            self.document_model
            .get_by_id(

                document_id

            )
        )


        if not document:

            return {

                "success": False,

                "message": "Document not found."

            }





        deleted = (
            self.document_model
            .delete(

                document_id

            )
        )



        if deleted == 0:

            return {

                "success": False,

                "message": "Document was not deleted."

            }





        return {

            "success": True,

            "message": "Document deleted successfully."

        }