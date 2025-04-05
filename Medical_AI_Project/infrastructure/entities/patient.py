from typing import List, Optional
from datetime import datetime

class Patient:
    """
    Сущность пациента.
    """

    def __init__(
        self,
        patient_id: int,
        full_name: str,
        age: int,
        gender: str,
        symptoms: List[str],
        chronic_conditions: Optional[List[str]] = None,
        medications: Optional[List[str]] = None,
        diagnosis: Optional[str] = None,
        confidence: Optional[float] = None
    ):
        self.patient_id = patient_id
        self.full_name = full_name
        self.age = age
        self.gender = gender
        self.symptoms = symptoms
        self.chronic_conditions = chronic_conditions or []
        self.medications = medications or []
        self.diagnosis = diagnosis
        self.confidence = confidence
        self.created_at = datetime.utcnow()

    def to_dict(self):
        """
        Конвертирует объект пациента в словарь для MongoDB.
        """
        return {
            "patient_id": self.patient_id,
            "full_name": self.full_name,
            "age": self.age,
            "gender": self.gender,
            "symptoms": self.symptoms,
            "chronic_conditions": self.chronic_conditions,
            "medications": self.medications,
            "diagnosis": self.diagnosis,
            "confidence": self.confidence,
            "created_at": self.created_at,
        }
