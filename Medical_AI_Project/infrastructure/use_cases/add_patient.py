from ..infrastructure.database.patient_repository import PatientRepository
from ..infrastructure.database.audit_repository import AuditRepository
from ..infrastructure.entities.patient import Patient


class AddPatientUseCase:
    """
    Use case для добавления нового пациента.
    """

    def execute(self, patient: Patient):
        """
        Выполняет добавление пациента в БД.
        """
        # Сохраняем пациента в БД
        PatientRepository.add_patient(patient)

        # Логируем операцию
        AuditRepository.log_operation(
            "Patient Added", f"Patient {patient.full_name} added to DB"
        )

        return {"message": "Patient added successfully", "patient_id": patient.patient_id}
