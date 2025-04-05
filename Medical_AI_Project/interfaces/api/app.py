from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from core.entities.medical_case import MedicalCase
from core.use_cases.diagnose_patient import DiagnosePatient
from modules.diagnostics.ai_diagnosis import AIDiagnosisFactory
from modules.nlp.nlp_model import NLPModelFactory
from infrastructure.logging.logger import Logger

# Инициализация FastAPI
app = FastAPI(title="Medical Diagnosis API", version="1.0")
logger = Logger("API")

# Загрузка моделей
ai_model = AIDiagnosisFactory.get_model("pytorch", "models/final/diagnosis_model.pth")
nlp_model = NLPModelFactory.get_model("bert")

# Подключение use-case для диагностики
diagnose_use_case = DiagnosePatient(ai_model, nlp_model)

class MedicalCaseRequest(BaseModel):
    patient_id: int
    full_name: str
    age: int
    gender: str
    symptoms: List[str]
    chronic_conditions: Optional[List[str]] = []
    medications: Optional[List[str]] = []
    preferred_language: Optional[str] = "English"

class DiagnosisResponse(BaseModel):
    patient_id: int
    diagnosis: str
    confidence: float

@app.post("/diagnosis", response_model=DiagnosisResponse)
async def diagnosis_patient(request: MedicalCaseRequest):
    """ API для диагностики пациента. """
    try:
        logger.info(f"Получен запрос на диагностику: {request.patient_id}")

        # Создание объекта медицинского случая
        medical_case = MedicalCase(
            patient_id=request.patient_id,
            full_name=request.full_name,
            age=request.age,
            gender=request.gender,
            symptoms=request.symptoms,
            chronic_conditions=request.chronic_conditions,
            medications=request.medications,
            preferred_language=request.preferred_language
        )

        # Выполнение диагностики
        result = diagnose_use_case.execute(medical_case)

        return DiagnosisResponse(**result)

    except Exception as e:
        logger.error(f"Ошибка в API: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")
