from infrastructure.database.patient_repository import PatientRepository
from infrastructure.database.log_repository import LogRepository
from entities.patient import Patient
from core.use_cases.diagnose_patient import DiagnosePatient
from modules.diagnostics.ai_diagnosis import AIDiagnosisFactory
from modules.nlp.nlp_model import NLPModelFactory
from modules.common.logger import Logger

logger = Logger("DiagnosePatient")

# Загрузка моделей
ai_model = AIDiagnosisFactory.get_model("pytorch", "models/final/diagnosis_model.pth")
nlp_model = NLPModelFactory.get_model("bert")

diagnose_use_case = DiagnosePatient(ai_model, nlp_model)

class DiagnosePatientUseCase:
    """
    Use case для диагностики пациента.
    """

    def execute(self, patient: Patient):
        """
        Выполняет диагностику пациента.
        """
        logger.info(f"Executing diagnosis for patient {patient.patient_id}")

        # Получение диагноза
        result = diagnose_use_case.execute(patient)

        # Обновление данных пациента
        patient.diagnosis = result["diagnosis"]
        patient.confidence = result["confidence"]

        # Сохранение пациента в БД
        PatientRepository.add_or_update_patient(patient)

        # Логирование операции
        LogRepository.log_operation("Diagnosis", f"Diagnosed patient {patient.patient_id}: {result['diagnosis']}")

        logger.info(f"Diagnosis for patient {patient.patient_id} saved in DB")

        return result
