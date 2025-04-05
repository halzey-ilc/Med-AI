from infrastructure.database.audit_repository import AuditRepository


class LogOperationUseCase:
    """
    Use case для логирования операций.
    """

    def execute(self, action: str, details: str):
        """
        Выполняет запись лога в БД.
        """
        AuditRepository.log_operation(action, details)
