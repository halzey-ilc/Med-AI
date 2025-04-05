from infrastructure.database.mongo_client import patients_collection
from datetime import datetime
from pymongo.errors import PyMongoError

class PatientRepository:
    """ Репозиторий для работы с пациентами в MongoDB. """

    @staticmethod
    def save_diagnosis(patient_id, diagnosis, confidence):
        """ Сохраняет диагноз пациента в БД. """
        try:
            patients_collection.update_one(
                {"patient_id": patient_id},
                {"$set": {
                    "diagnosis": diagnosis,
                    "confidence": confidence,
                    "updated_at": datetime.utcnow()
                }},
                upsert=True
            )
        except PyMongoError as e:
            raise Exception(f"Ошибка при сохранении диагноза: {str(e)}")
