import unittest
import numpy as np
import sys

# Добавляем корневой путь проекта, если тесты запущены не из корня
sys.path.append("..")

from core.entities.medical_case import MedicalCase
from modules.diagnostics.ai_diagnosis import AIDiagnosisFactory
from modules.nlp.nlp_model import NLPModelFactory
from core.use_cases.diagnose_patient import DiagnosePatient


class TestDiagnosePatient(unittest.TestCase):
    """
    Unit tests for diagnosing patients using AI.
    """

    @classmethod
    def setUpClass(cls):
        """
        Runs once before all tests. Loads models.
        """
        cls.ai_model = AIDiagnosisFactory.get_model("pytorch", "models/final/diagnosis_model.pth")
        cls.nlp_model = NLPModelFactory.get_model("bert")  # Загружаем NLP модель
        cls.diagnose_use_case = DiagnosePatient(cls.ai_model, cls.nlp_model)

    def setUp(self):
        """
        Runs before each test case. Creates a sample patient case.
        """
        self.medical_case = MedicalCase(
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

    def test_diagnosis_output_format(self):
        """
        Test if the diagnosis result has the correct structure.
        """
        result = self.diagnose_use_case.execute(self.medical_case)
        self.assertIn("diagnosis", result)
        self.assertIn("confidence", result)
        self.assertIsInstance(result["diagnosis"], str)
        self.assertIsInstance(result["confidence"], float)

    def test_confidence_score_range(self):
        """
        Ensure the confidence score is between 0 and 1.
        """
        result = self.diagnose_use_case.execute(self.medical_case)
        self.assertGreaterEqual(result["confidence"], 0.0)
        self.assertLessEqual(result["confidence"], 1.0)

    def test_prediction_with_empty_symptoms(self):
        """
        Check if the model handles empty symptoms correctly.
        """
        self.medical_case.symptoms = []
        result = self.diagnose_use_case.execute(self.medical_case)
        self.assertNotEqual(result["diagnosis"], "Error in Diagnosis")

    def test_prediction_with_random_symptoms(self):
        """
        Test diagnosis when given random symptoms.
        """
        self.medical_case.symptoms = ["random_symptom_123", "unknown_disease"]
        result = self.diagnose_use_case.execute(self.medical_case)
        self.assertNotEqual(result["diagnosis"], "Error in Diagnosis")


if __name__ == "__main__":
    unittest.main()
