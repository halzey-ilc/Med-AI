from core.entities.medical_case import MedicalCase
from modules.diagnostics.ai_diagnosis import AIDiagnosis
from modules.nlp.nlp_model import NLPModel
from modules.common.logger import Logger


class DiagnosePatient:
    """
    Use case for diagnosing a patient based on medical data.
    """

    def __init__(self, ai_model: AIDiagnosis, nlp_model: NLPModel):
        self.ai_model = ai_model
        self.nlp_model = nlp_model
        self.logger = Logger("diagnose_patient")

    def execute(self, medical_case: MedicalCase) -> dict:
        """
        Diagnose a patient based on their symptoms and medical history.

        :param medical_case: A MedicalCase object containing patient data.
        :return: Dictionary containing diagnosis and confidence score.
        """
        self.logger.info(f"Processing diagnosis for patient: {medical_case.patient_id}")

        # Обрабатываем симптомы через NLP
        symptoms_text = " ".join(medical_case.symptoms)
        symptoms_vector = self.nlp_model.process_text(symptoms_text)

        # Объединяем данные для модели
        model_input = {
            "age": medical_case.age,
            "gender": medical_case.gender,
            "symptoms_vector": symptoms_vector,
            "chronic_conditions": medical_case.chronic_conditions,
            "medications": medical_case.medications
        }

        # Получаем предсказание от ИИ-модели
        diagnosis, confidence = self.ai_model.predict(model_input)

        self.logger.info(f"Diagnosis completed: {diagnosis} (Confidence: {confidence})")

        return {
            "patient_id": medical_case.patient_id,
            "diagnosis": diagnosis,
            "confidence": confidence
        }


# Example Usage
if __name__ == "__main__":
    from modules.diagnostics.ai_diagnosis import AIDiagnosis
    from modules.nlp.nlp_model import NLPModel
    from core.entities.medical_case import MedicalCase

    # Загружаем модели
    ai_model = AIDiagnosis(model_path="models/final/diagnosis_model.pth")
    nlp_model = NLPModel()

    # Создаём экземпляр use case
    diagnose_use_case = DiagnosePatient(ai_model, nlp_model)

    # Пример медицинского случая
    medical_case = MedicalCase(
        patient_id=1,
        full_name="John Doe",
        passport_id="AB1234567",
        phone_number="1234567890",
        address="123 Main St, City, Country",
        email="johndoe@example.com",
        age=35,
        gender="male",
        symptoms=["fever", "cough", "headache"],
        chronic_conditions=["Hypertension"],
        medications=["Metformin"]
    )

    # Диагностируем пациента
    result = diagnose_use_case.execute(medical_case)
    print(result)


    #✔ Используется чистая архитектура → Код отделен от инфраструктуры и моделей.
    #✔ Добавлено логирование → Отслеживаем процесс диагностики.
    #✔ Модуль легко расширяем → Можно менять ai_diagnosis или nlp_model без переписывания логики.
    #✔ Интегрирован NLP → Модель обрабатывает текстовые симптомы перед передачей в AIDiagnosis.




