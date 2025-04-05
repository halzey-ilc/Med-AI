from .mongo_client import logs_collection
from datetime import datetime

class LogRepository:
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
        logs_collection.insert_one(log_entry)
        print(f"🔍 Log recorded: {action}")
