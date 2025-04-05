from mongo_client import audit_logs_collection
from datetime import datetime


class AuditRepository:
    """
    Репозиторий логов операций.
    """

    @staticmethod
    def log_operation(action: str, details: str):
        """
        Логирует операцию в MongoDB.
        """
        log_entry = {
            "action": action,
            "details": details,
            "timestamp": datetime.utcnow(),
        }
        audit_logs_collection.insert_one(log_entry)
        print(f"🔍 Log recorded: {action}")
