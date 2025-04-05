from pymongo import MongoClient
import os

# Подключение к MongoDB
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
client = MongoClient(MONGO_URI)
db = client["medical_db"]

# Коллекции в MongoDB
patients_collection = db["patient_records"]
diagnoses_collection = db["diagnoses"]
doctors_collection = db["doctors"]
appointments_collection = db["appointments"]
chatbot_interactions_collection = db["chatbot_interactions"]
medical_notes_collection = db["medical_notes"]
references_collection = db["references"]
audit_logs_collection = db["audit_logs"]
cache_collection = db["cache"]

# Индексы
patients_collection.create_index("patient_id", unique=True)
