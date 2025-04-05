import re
import numpy as np
import torch
import sys
import os
from abc import ABC, abstractmethod
from typing import Dict, Any
from modules.common.logger import Logger
from sklearn.feature_extraction.text import TfidfVectorizer
from transformers import BertTokenizer, BertModel
from modules.common.logger import Logger

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

class INLPModel(ABC):
    """Interface for all NLP models handling medical text processing."""

    @abstractmethod
    def preprocess_text(self, text: str) -> str:
        """Cleans and normalizes the input text."""
        pass

    @abstractmethod
    def text_to_vector(self, text: str) -> np.ndarray:
        """Converts text into a numerical vector representation."""
        pass


class TfidfNLPModel(INLPModel):
    """NLP model based on TF-IDF with caching."""

    def __init__(self):
        self.logger = Logger("TfidfNLPModel")
        self.logger.info("Initializing TF-IDF NLP model...")
        self.vectorizer = TfidfVectorizer(max_features=100)
        self.text_cache = {}  # Caching text vectors
        self.logger.info("TF-IDF model initialized.")

    def preprocess_text(self, text: str) -> str:
        """Cleans and normalizes text."""
        text = text.lower()
        text = re.sub(r"[^a-zA-Zа-яА-Я0-9\s]", "", text)
        return text.strip()

    def text_to_vector(self, text: str) -> np.ndarray:
        """Converts text into a TF-IDF vector (with caching)."""
        cleaned_text = self.preprocess_text(text)
        if cleaned_text in self.text_cache:
            return self.text_cache[cleaned_text]  # Return cached vector

        vector = self.vectorizer.fit_transform([cleaned_text]).toarray()
        vector = vector[0] if len(vector) > 0 else np.zeros(100)
        self.text_cache[cleaned_text] = vector  # Store in cache
        return vector


class BertNLPModel(INLPModel):
    """NLP model based on BERT."""

    def __init__(self):
        self.logger = Logger("BertNLPModel")
        self.logger.info("Loading BERT model...")
        self.tokenizer = BertTokenizer.from_pretrained("bert-base-uncased")
        self.model = BertModel.from_pretrained("bert-base-uncased")
        self.logger.info("BERT model loaded successfully.")

    def preprocess_text(self, text: str) -> str:
        """Cleans the input text before BERT processing."""
        return text.lower().strip()

    def text_to_vector(self, text: str) -> np.ndarray:
        """Converts text into a BERT embedding."""
        cleaned_text = self.preprocess_text(text)
        inputs = self.tokenizer(cleaned_text, return_tensors="pt", truncation=True, padding=True, max_length=50)
        with torch.no_grad():
            outputs = self.model(**inputs)
        return outputs.last_hidden_state[:, 0, :].numpy().flatten()


class NLPModelFactory:
    """Factory for creating NLP models."""

    @staticmethod
    def get_model(model_type: str) -> INLPModel:
        """Creates an NLP model instance."""
        if model_type == "tfidf":
            return TfidfNLPModel()
        elif model_type == "bert":
            return BertNLPModel()
        else:
            raise ValueError(f"Unknown NLP model type: {model_type}")


# Example Usage
if __name__ == "__main__":
    # Creating an NLP model via the factory
    nlp_model = NLPModelFactory.get_model("tfidf")

    test_text = "Patient reports fever, cough, and shortness of breath."
    vector = nlp_model.text_to_vector(test_text)
    print("Feature vector:", vector[:10])  # Displaying the first 10 elements of the vector
