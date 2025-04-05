from core.use_cases.diagnose_patient import DiagnosePatient
from core.entities.medical_case import MedicalCase
from modules.diagnostics.ai_diagnosis import AIDiagnosisFactory
from modules.nlp.nlp_model import NLPModelFactory

if __name__ == "__main__":
    # Загружаем модели
    ai_model = AIDiagnosisFactory.get_model("pytorch", "models/final/diagnosis_model.pth")
    nlp_model = NLPModelFactory.get_model("bert")

    # Создаём экземпляр юз-кейса
    diagnose_use_case = DiagnosePatient(ai_model, nlp_model)

    # Тестовый медицинский случай
    medical_case = MedicalCase(
        patient_id=1,
        full_name="John Doe",
        passport_id="N/A",
        phone_number="N/A",
        address="N/A",
        email="N/A",
        age=35,
        gender="male",
        symptoms=["fever", "cough", "headache"],
        chronic_conditions=["Hypertension"],
        medications=["Metformin"]
    )

    # Запускаем диагностику
    result = diagnose_use_case.execute(medical_case)
    print(result)
