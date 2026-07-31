from database.patient_professional import PatientProfessional


class PatientProfessionalService:


    @staticmethod
    def create_link(patient_id, professional_id):

        # verifica se já existe vínculo
        existing_links = PatientProfessional.get_by_patient(patient_id)

        for link in existing_links:
            if link.professional_id == professional_id:
                return None


        relationship = PatientProfessional(
            patient_id=patient_id,
            professional_id=professional_id
        )

        relationship.save()

        return relationship



    @staticmethod
    def get_patient_professionals(patient_id):

        return PatientProfessional.get_by_patient(patient_id)



    @staticmethod
    def get_professional_patients(professional_id):

        return PatientProfessional.get_by_professional(professional_id)



    @staticmethod
    def deactivate_link(link_id):

        relationship = PatientProfessional.get_by_id(link_id)

        if not relationship:
            return False


        relationship.deactivate()

        return True