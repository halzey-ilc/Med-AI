import random
import faker
from datetime import datetime, timedelta
from typing import List, Dict, Any


class DataRawGenerator:
    """
    A class to generate raw medical case data for testing and simulation.
    """

    def __init__(self):
        self.fake = faker.Faker()

    def generate_random_case(self) -> Dict[str, Any]:
        """
        Generate a single random medical case with potentially incorrect or missing data.

        :return: Dictionary containing raw medical case data.
        """
        gender = random.choice(["male", "female", "other", "unknown"])
        age = random.choice([random.randint(0, 120), None, -5, 200])  # Some incorrect values

        raw_case = {
            "patient_id": random.randint(1000, 9999),
            "full_name": self.fake.name(),
            "passport_id": self.fake.bothify("??######"),
            "phone_number": random.choice([self.fake.phone_number(), "12345", None]),
            "address": self.fake.address(),
            "email": self.fake.email(),
            "age": age,
            "gender": gender,
            "symptoms": random.sample(["fever", "cough", "headache", "fatigue", "nausea"], k=random.randint(1, 3)),
            "medical_history": random.choice(["Diabetes", "Hypertension", None, "Asthma"]),
            "attending_physician": self.fake.name(),
            "last_visit": self.random_date(),
            "chatbot_interactions": random.sample(
                ["Asked about symptoms", "Requested appointment", "Inquired about medications"], k=random.randint(0, 3)
            ),
            "blood_type": random.choice(["A+", "A-", "B+", "B-", "O+", "O-", "AB+", "AB-", None]),
            "allergies": random.sample(["Penicillin", "Pollen", "Peanuts", "Dust"], k=random.randint(0, 2)),
            "chronic_conditions": random.sample(["Heart Disease", "Arthritis", "Depression"], k=random.randint(0, 2)),
            "medications": random.sample(["Metformin", "Ibuprofen", "Lisinopril"], k=random.randint(0, 2)),
            "preferred_language": random.choice(["English", "Spanish", "French", "Russian"]),
            "interaction_history_summary": random.choice(["Patient frequently asks about flu symptoms", None]),
            "study_notes": random.choice(["Important case for study", None]),
            "references": random.sample(
                ["https://www.ncbi.nlm.nih.gov/pubmed/12345678", "https://www.who.int/health-topics"],
                k=random.randint(0, 2)
            ),
        }

        return raw_case

    def generate_bulk_cases(self, num_cases: int = 10) -> List[Dict[str, Any]]:
        """
        Generate multiple random medical cases.

        :param num_cases: Number of cases to generate.
        :return: List of raw medical cases.
        """
        return [self.generate_random_case() for _ in range(num_cases)]

    @staticmethod
    def random_date() -> str:
        """
        Generate a random past date or an invalid date.

        :return: A string representing a random date in 'YYYY-MM-DD' format or 'Invalid'.
        """
        if random.random() < 0.2:
            return "2024-02-30"  # Invalid date
        random_days = random.randint(1, 365 * 5)  # Up to 5 years in the past
        return (datetime.today() - timedelta(days=random_days)).strftime("%Y-%m-%d")


# Example Usage
if __name__ == "__main__":
    generator = DataRawGenerator()

    # Generate a single random case
    single_case = generator.generate_random_case()
    print("Example Raw Case:\n", single_case)

    # Generate multiple cases
    bulk_cases = generator.generate_bulk_cases(5)
    print("\nGenerated Bulk Cases:")
    for case in bulk_cases:
        print(case)
