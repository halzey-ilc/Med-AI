import unittest
from fastapi.testclient import TestClient
from interfaces.api.app import app

# uvicorn interfaces.api.app:app --host 0.0.0.0 --port 8000 --reload
# это запуск апи

class TestApi(unittest.TestCase):
    """
    Unit tests for the Medical Diagnosis API
    """
    @classmethod
    def setUpClass(cls):
        """
        Runs once before all tests. Initializes API test client
        """
        cls.client = TestClient(app)

        def test_successful_diagnosis(self):
            """
            Test a successful diagnosis request with valid data.
            """
            response = self.client.post("/diagnose", json={
                "patient_id": 1,
                "full_name": "John Doe",
                "age": 35,
                "gender": "male",
                "symptoms": ["fever", "cough", "headache"],
                "chronic_conditions": ["Hypertension"],
                "medications": ["Metformin"]
            })
            self.assertEqual(response.status_code, 200)
            data = response.json()
            self.assertIn("diagnosis", data)
            self.assertIn("confidence", data)
            self.assertIsInstance(data["diagnosis"], str)
            self.assertIsInstance(data["confidence"], float)

        def test_missing_symptoms(self):
            """
            Test a request missing the required 'symptoms' field.
            """
            response = self.client.post("/diagnose", json={
                "patient_id": 2,
                "full_name": "Jane Doe",
                "age": 29,
                "gender": "female"
            })
            self.assertEqual(response.status_code, 422)  # Unprocessable Entity

        def test_invalid_data_format(self):
            """
            Test a request with an invalid data format.
            """
            response = self.client.post("/diagnose", json={
                "patient_id": "invalid_id",  # Should be an integer
                "full_name": "Invalid Patient",
                "age": "thirty",  # Should be an integer
                "gender": "unknown",
                "symptoms": "cough",  # Should be a list
                "chronic_conditions": "None",  # Should be a list
                "medications": None
            })
            self.assertEqual(response.status_code, 422)  # Unprocessable Entity

    if __name__ == "__main__":
        unittest.main()


# python -m unittest tests/test_api.py
# Запуст юнит теста


