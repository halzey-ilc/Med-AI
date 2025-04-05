# from fastapi import FastAPI, HTTPException
# from pydantic import BaseModel
# from typing import List, Optional
# from datetime import datetime
# from pymongo import MongoClient
# from core.entities.medical_case import MedicalCase
# from core.use_cases.diagnose_patient import DiagnosePatient
# from modules.diagnostics.ai_diagnosis import AIDiagnosisFactory
# from modules.nlp.nlp_model import NLPModelFactory
# from modules.common.logger import Logger
#
# # Подключение к MongoDB
# MONGO_URI = "mongodb://localhost:27017/"
# client = MongoClient(MONGO_URI)
# db = client["medical_db"]
# patients_collection = db["patient_records"]
# logs_collection = db["logs"]
#
# # Уникальный индекс для patient_id
# patients_collection.create_index("patient_id", unique=True)
#
# # Инициализация FastAPI
# app = FastAPI(title="Medical Diagnosis API", version="1.0")
# logger = Logger("API")
#
# # Загрузка моделей
# ai_model = AIDiagnosisFactory.get_model("pytorch", "models/final/diagnosis_model.pth")
# nlp_model = NLPModelFactory.get_model("bert")
#
# # Подключение use-case для диагностики
# diagnose_use_case = DiagnosePatient(ai_model, nlp_model)
#
#
# class MedicalCaseRequest(BaseModel):
#     patient_id: int
#     full_name: str
#     age: int
#     gender: str
#     symptoms: List[str]
#     chronic_conditions: Optional[List[str]] = []
#     medications: Optional[List[str]] = []
#     preferred_language: Optional[str] = "English"
#
#
# class DiagnosisResponse(BaseModel):
#     patient_id: int
#     diagnosis: str
#     confidence: float
#
#
# def log_operation(action, details):
#     """ Логирует операции в базе данных."""
#     log_entry = {
#         "action": action,
#         "details": details,
#         "timestamp": datetime.utcnow()
#     }
#     logs_collection.insert_one(log_entry)
#     logger.info(f"Log: {action} - {details}")
#
#
# @app.post("/diagnosis", response_model=DiagnosisResponse)
# async def diagnosis_patient(request: MedicalCaseRequest):
#     """ API для диагностики пациента."""
#     try:
#         logger.info(f"Received diagnosis request for patient: {request.patient_id}")
#
#         # Создание медицинского случая
#         medical_case = MedicalCase(
#             patient_id=request.patient_id,
#             full_name=request.full_name,
#             age=request.age,
#             gender=request.gender,
#             symptoms=request.symptoms,
#             chronic_conditions=request.chronic_conditions,
#             medications=request.medications,
#             preferred_language=request.preferred_language
#         )
#
#         # Получение диагноза
#         result = diagnose_use_case.execute(medical_case)
#
#         # Обновление записи пациента в MongoDB
#         patients_collection.update_one(
#             {"patient_id": request.patient_id},
#             {"$set": {"diagnosis": result["diagnosis"], "confidence": result["confidence"]}},
#             upsert=True
#         )
#
#         log_operation("Diagnosis", f"Diagnosed patient {request.patient_id}: {result['diagnosis']}")
#
#         return DiagnosisResponse(**result)
#
#     except Exception as e:
#         logger.error(f"Error during diagnosis: {e}")
#         raise HTTPException(status_code=500, detail="Internal server error")
#
#
# # if __name__ == "__main__":
# #     import uvicorn
# #     logger.info("Starting API service...")
# #     uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
