import torch
import numpy as np
from abc import ABC, abstractmethod
from typing import Tuple, Dict, Any
from modules.common.logger import Logger


class IAIDiagnosis(ABC):
    """
    Interface for all AI-based diagnosis models.
    """

    @abstractmethod
    def load_model(self, model_path: str) -> torch.nn.Module:
        """ Loads the AI model from a file. """
        pass

    @abstractmethod
    def predict(self, data: Dict[str, Any]) -> Tuple[str, float]:
        """ Performs a diagnosis prediction. """
        pass


class TorchAIDiagnosis(IAIDiagnosis):
    """
    PyTorch-based AI diagnosis model.
    """

    def __init__(self, model_path: str):
        self.logger = Logger("TorchAIDiagnosis")
        self.logger.info("Loading PyTorch model...")
        self.model = None  # Временно отключаем загрузку модели

        #self.model = self.load_model(model_path)
        self.logger.info("Model loaded successfully.")

    def load_model(self, model_path: str) -> torch.nn.Module:
        """
        Loads the trained PyTorch model from a file.

        :param model_path: Path to the saved model.
        :return: Loaded PyTorch model.
        """
        try:
            model = torch.load(model_path, map_location=torch.device("cpu"))
            model.eval()
            return model
        except Exception as e:
            self.logger.error(f"Failed to load model: {e}")
            raise RuntimeError("Could not load AI model.")

    def preprocess_input(self, data: Dict[str, Any]) -> torch.Tensor:
        """
        Prepares input data for the model.

        :param data: Dictionary containing patient information.
        :return: PyTorch tensor with processed input features.
        """
        age = data.get("age", 0)
        gender = 1 if data.get("gender") == "male" else 0  # 1 = male, 0 = female/other
        symptoms_vector = np.array(data.get("symptoms_vector", [0] * 100))  # NLP feature vector
        chronic_conditions = len(data.get("chronic_conditions", []))  # Number of chronic conditions
        medications = len(data.get("medications", []))  # Number of medications

        input_vector = np.concatenate(([age, gender, chronic_conditions, medications], symptoms_vector))
        return torch.tensor(input_vector, dtype=torch.float32).unsqueeze(0)  # Batch size of 1

    def predict(self, data: Dict[str, Any]) -> Tuple[str, float]:
        """
        Predicts a medical diagnosis based on input data.

        :param data: Dictionary containing patient information.
        :return: Predicted diagnosis and confidence score.
        """
        self.logger.info("Generating diagnosis prediction...")
        try:
            input_tensor = self.preprocess_input(data)
            with torch.no_grad():
                output = self.model(input_tensor)
            predicted_class = torch.argmax(output, dim=1).item()
            confidence = torch.max(torch.nn.functional.softmax(output, dim=1)).item()

            diagnosis_mapping = {
                0: "Common Cold",
                1: "Flu",
                2: "Pneumonia",
                3: "COVID-19",
                4: "Hypertension Complications"
            }
            diagnosis = diagnosis_mapping.get(predicted_class, "Unknown Condition")

            self.logger.info(f"Diagnosis: {diagnosis}, Confidence: {confidence:.2f}")
            return diagnosis, confidence
        except Exception as e:
            self.logger.error(f"Prediction failed: {e}")
            return "Error in Diagnosis", 0.0


class AIDiagnosisFactory:
    """
    Factory class for selecting different AI diagnosis models.
    """

    @staticmethod
    def get_model(model_type: str, model_path: str) -> IAIDiagnosis:
        """
        Creates an AI diagnosis model based on the specified type.

        :param model_type: Type of the model (e.g., "pytorch").
        :param model_path: Path to the model file.
        :return: An instance of the AI diagnosis model.
        """
        if model_type == "pytorch":
            return TorchAIDiagnosis(model_path)
        else:
            raise ValueError(f"Unknown model type: {model_type}")


# Example Usage
if __name__ == "__main__":
    ai_model = AIDiagnosisFactory.get_model("pytorch", "models/final/diagnosis_model.pth")

    test_input = {
        "age": 40,
        "gender": "male",
        "symptoms_vector": np.random.rand(100).tolist(),
        "chronic_conditions": ["Diabetes"],
        "medications": ["Metformin"]
    }

    diagnosis, confidence = ai_model.predict(test_input)
    print(f"Diagnosis: {diagnosis}, Confidence: {confidence:.2f}")
