import re
from datetime import datetime
from typing import List, Optional


class DataPreprocessor:
    """
    A class to preprocess and clean medical case data before analysis.
    """

    @staticmethod
    def clean_text(text: Optional[str]) -> str:
        """
        Cleans and normalizes a given text input.
        - Converts to lowercase
        - Strips leading and trailing spaces
        - Removes extra whitespace

        :param text: Input text
        :return: Cleaned text
        """
        if not text:
            return "N/A"
        return re.sub(r"\s+", " ", text.strip().lower())

    @staticmethod
    def validate_age(age: Optional[int]) -> int:
        """
        Ensures the age is within a reasonable range.

        :param age: Age value
        :return: Validated age
        """
        if not age or age < 0 or age > 120:
            return -1  # -1 означает неизвестный возраст
        return age

    @staticmethod
    def standardize_gender(gender: Optional[str]) -> str:
        """
        Standardizes gender input to 'male', 'female', or 'other'.

        :param gender: Input gender value
        :return: Standardized gender
        """
        valid_genders = {"male", "female", "other"}
        gender = DataPreprocessor.clean_text(gender)
        return gender if gender in valid_genders else "other"

    @staticmethod
    def format_date(date_str: Optional[str]) -> str:
        """
        Formats a date string into YYYY-MM-DD format.

        :param date_str: Input date string
        :return: Standardized date format or "Unknown" if invalid
        """
        if not date_str:
            return "Unknown"

        try:
            date_obj = datetime.strptime(date_str, "%Y-%m-%d")
            return date_obj.strftime("%Y-%m-%d")
        except ValueError:
            return "Unknown"

    @staticmethod
    def validate_phone_number(phone_number: Optional[str]) -> str:
        """
        Ensures the phone number is valid (10-15 digits).

        :param phone_number: Input phone number
        :return: Validated phone number or "Invalid"
        """
        if not phone_number or not re.fullmatch(r"\d{10,15}", phone_number):
            return "Invalid"
        return phone_number

    @staticmethod
    def validate_list(input_list: Optional[List[str]]) -> List[str]:
        """
        Ensures a list is valid. If None, returns an empty list.

        :param input_list: Input list
        :return: Valid list
        """
        return input_list if isinstance(input_list, list) else []

    @staticmethod
    def preprocess_medical_case(data: dict) -> dict:
        """
        Cleans and preprocesses a medical case dictionary.

        :param data: Raw input dictionary
        :return: Cleaned and validated dictionary
        """
        return {
            "patient_id": data.get("patient_id", "Unknown"),
            "full_name": DataPreprocessor.clean_text(data.get("full_name")),
            "passport_id": data.get("passport_id", "Unknown"),
            "phone_number": DataPreprocessor.validate_phone_number(data.get("phone_number")),
            "address": DataPreprocessor.clean_text(data.get("address")),
            "email": DataPreprocessor.clean_text(data.get("email")),
            "age": DataPreprocessor.validate_age(data.get("age")),
            "gender": DataPreprocessor.standardize_gender(data.get("gender")),
            "symptoms": DataPreprocessor.validate_list(data.get("symptoms")),
            "medical_history": DataPreprocessor.clean_text(data.get("medical_history")),
            "attending_physician": DataPreprocessor.clean_text(data.get("attending_physician")),
            "last_visit": DataPreprocessor.format_date(data.get("last_visit")),
            "chatbot_interactions": DataPreprocessor.validate_list(data.get("chatbot_interactions")),
            "blood_type": data.get("blood_type", "Unknown"),
            "allergies": DataPreprocessor.validate_list(data.get("allergies")),
            "chronic_conditions": DataPreprocessor.validate_list(data.get("chronic_conditions")),
            "medications": DataPreprocessor.validate_list(data.get("medications")),
            "preferred_language": DataPreprocessor.clean_text(data.get("preferred_language")),
            "interaction_history_summary": DataPreprocessor.clean_text(data.get("interaction_history_summary")),
            "study_notes": DataPreprocessor.clean_text(data.get("study_notes")),
            "references": DataPreprocessor.validate_list(data.get("references")),
        }


# Example Usage
if __name__ == "__main__":
    raw_data = {
        "patient_id": 1,
        "full_name": "   John DOE   ",
        "passport_id": "AB1234567",
        "phone_number": "1234567890",
        "address": " 123 Main St, City, Country  ",
        "email": "John.Doe@Example.Com",
        "age": 200,  # Invalid
        "gender": "Male",
        "symptoms": ["fever", "cough", " headache"],
        "medical_history": " Diabetes  ",
        "attending_physician": "Dr. Smith ",
        "last_visit": "2024-02-30",  # Invalid date
        "blood_type": "O+",
        "allergies": [" Penicillin "],
        "chronic_conditions": None,
        "medications": ["Metformin"],
        "preferred_language": "ENGLISH",
        "interaction_history_summary": None,
        "study_notes": "   Case study on hypertension.",
        "references": ["https://www.ncbi.nlm.nih.gov/pubmed/12345678"],
    }

    cleaned_data = DataPreprocessor.preprocess_medical_case(raw_data)
    print(cleaned_data)
