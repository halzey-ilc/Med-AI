from fastapi import FastAPI, HTTPException
from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime
from pymongo import MongoClient

# Подключение к MongoDB
MONGO_URI = "mongodb://localhost:27017/"
client = MongoClient(MONGO_URI)
db = client["medical_db"]
patients_collection = db["patient_records"]

# Инициализация FastAPI
app = FastAPI(title="Medical Diagnosis API", version="1.0")


#  Определяем схему запроса
class PatientRequest(BaseModel):
    patient_id: int
    full_name: str
    age: int
    gender: str
    symptoms: List[str]
    chronic_conditions: Optional[List[str]] = []
    medications: Optional[List[str]] = []
    diagnosis: Optional[str] = None
    confidence: Optional[float] = None
    created_at: Optional[datetime] = datetime.utcnow()


#  1. **Добавление пациента**
@app.post("/patients/", response_model=dict)
async def add_patient(request: PatientRequest):
    if patients_collection.find_one({"patient_id": request.patient_id}):
        raise HTTPException(status_code=400, detail="Patient already exists")

    patient_data = request.dict()
    patients_collection.insert_one(patient_data)
    return {"message": f"Patient {request.full_name} added successfully!"}


#  2. **Получение пациента по ID**
@app.get("/patients/{patient_id}", response_model=dict)
async def get_patient(patient_id: int):
    patient = patients_collection.find_one({"patient_id": patient_id})
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")

    return {k: v for k, v in patient.items() if k != "_id"}  # Убираем MongoDB `_id`


#  3. **Обновление данных пациента**
@app.put("/patients/update/{patient_id}", response_model=dict)
async def update_patient(patient_id: int, updates: dict):
    result = patients_collection.update_one({"patient_id": patient_id}, {"$set": updates})
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Patient not found")

    return {"message": f"Patient {patient_id} updated successfully!"}


#  4. **Удаление пациента**
@app.delete("/patients/delete/{patient_id}", response_model=dict)
async def delete_patient(patient_id: int):
    result = patients_collection.delete_one({"patient_id": patient_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Patient not found")

    return {"message": f"Patient {patient_id} deleted successfully!"}


#  Эндпоинт для добавления пациента
@app.post("/patients/", status_code=201)
async def add_patient(patient: PatientRequest):
    if patients_collection.find_one({"patient_id": patient.patient_id}):
        raise HTTPException(status_code=400, detail="Patient already exists")

    patient_data = patient.dict()
    patient_data["created_at"] = datetime.utcnow()
    patients_collection.insert_one(patient_data)
    return {"message": "Patient added successfully", "patient": patient_data}


#  Эндпоинт для получения пациента по ID
@app.get("/patients/{patient_id}")
async def get_patient(patient_id: int):
    patient = patients_collection.find_one({"patient_id": patient_id}, {"_id": 0})
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    return patient


# Запуск FastAPI
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
