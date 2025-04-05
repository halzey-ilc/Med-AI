import uvicorn
from interfaces.api import app
from infrastructure.database.mongo_client import init_db

if __name__ == "__main__":
    print("✅ Initializing the database...")
    init_db()
    print("✅ Database initialized successfully.")
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
