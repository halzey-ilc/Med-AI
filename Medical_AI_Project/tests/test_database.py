import unittest
from sqlalchemy.orm import Session
from infrastructure.database.db_client import SessionLocal, PatientRecord, init_db

class TestDatabase(unittest.TestCase):
    """Тестирование базы данных."""

    @classmethod
    def setUpClass(cls):
        """Подключение к тестовой БД перед запуском тестов."""
        init_db()
        cls.db: Session = SessionLocal()

    def test_insert_patient(self):
        """Проверка записи нового пациента в БД."""
        new_patient = PatientRecord(
            patient_id=99,
            full_name="Test Patient",
            age=30,
            gender="male",
            symptoms=["cough", "fever"],
            chronic_conditions=["Diabetes"],
            medications=["Metformin"],
            diagnosis="Flu",
            confidence="0.85"
        )
        self.db.add(new_patient)
        self.db.commit()

        # Проверяем, что запись добавилась
        patient = self.db.query(PatientRecord).filter_by(patient_id=99).first()
        self.assertIsNotNone(patient)
        self.assertEqual(patient.full_name, "Test Patient")

    def test_read_patient(self):
        """Проверка чтения пациента из БД."""
        patient = self.db.query(PatientRecord).filter_by(patient_id=99).first()
        self.assertIsNotNone(patient)
        self.assertEqual(patient.diagnosis, "Flu")

    @classmethod
    def tearDownClass(cls):
        """Очистка БД после тестов."""
        cls.db.query(PatientRecord).filter_by(patient_id=99).delete()
        cls.db.commit()
        cls.db.close()


if __name__ == "__main__":
    unittest.main()




# Это Запуск теста
# python -m unittest tests/test_database.py
