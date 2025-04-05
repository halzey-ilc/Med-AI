from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class MedicalCase:
    """
    Represents a medical case with patient information and symptoms.
    Core entity in the system.
    """
    patient_id: int
    full_name: str
    passport_id: str
    phone_number: str
    address: str
    email: str
    age: int
    gender: str
    symptoms: List[str]
    medical_history: Optional[str] = None
    attending_physician: Optional[str] = None
    last_visit: Optional[str] = None
    chatbot_interactions: List[str] = field(default_factory=list)
    blood_type: Optional[str] = None
    allergies: List[str] = field(default_factory=list)
    chronic_conditions: List[str] = field(default_factory=list)
    medications: List[str] = field(default_factory=list)
    preferred_language: str = "English"
    interaction_history_summary: Optional[str] = None
    study_notes: Optional[str] = None
    references: List[str] = field(default_factory=list)

    def __post_init__(self):
        """
        Normalize gender field and handle empty lists correctly.
        """
        self.gender = self.gender.lower()

    def to_dict(self) -> dict:
        """
        Convert the medical case to a dictionary representation.
        """
        return self.__dict__

    def add_chatbot_interaction(self, interaction: str):
        """
        Add a chatbot interaction to the patient record.
        """
        self.chatbot_interactions.append(interaction)

    def add_study_notes(self, note: str):
        """
        Add a study note related to this case.
        """
        if self.study_notes:
            self.study_notes += f"\n{note}"
        else:
            self.study_notes = note

    def add_reference(self, reference: str):
        """
        Add a reference to the medical case.
        """
        self.references.append(reference)

    def __repr__(self):
        return f"<MedicalCase patient_id={self.patient_id}, name={self.full_name}, diagnosis={self.medical_history}>"
