from core.entities.medical_case import MedicalCase
from modules.diagnostics.ai_diagnosis import IAIDiagnosis
from modules.nlp.nlp_model import INLPModel
from modules.common.logger import Logger

class DiagnosePatient:
    """
    Use case для диагностики пациента на основе медицинских данных.
    """

    def __init__(self, ai_model: IAIDiagnosis, nlp_model: INLPModel):
        self.ai_model = ai_model
        self.nlp_model = nlp_model
        self.logger = Logger("DiagnosePatient")

    def execute(self, medical_case: MedicalCase) -> dict:
        """
        Выполняет диагностику пациента.

        :param medical_case: Данные пациента.
        :return: Словарь с диагнозом и уровнем уверенности.
        """
        self.logger.info(f"Начало диагностики для пациента {medical_case.patient_id}")

        # NLP обработка симптомов
        symptoms_text = " ".join(medical_case.symptoms)
        symptoms_vector = self.nlp_model.text_to_vector(symptoms_text)

        # Формируем входные данные для AI-модели
        model_input = {
            "age": medical_case.age,
            "gender": medical_case.gender,
            "symptoms_vector": symptoms_vector,
            "chronic_conditions": medical_case.chronic_conditions,
            "medications": medical_case.medications
        }

        # Получаем диагноз от AI-модели
        diagnosis, confidence = self.ai_model.predict(model_input)

        self.logger.info(f"Диагноз поставлен: {diagnosis} (Уверенность: {confidence:.2f})")

        return {
            "patient_id": medical_case.patient_id,
            "diagnosis": diagnosis,
            "confidence": confidence
        }
