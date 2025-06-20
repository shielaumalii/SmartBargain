# init_db.py
from core.backend.database import create_tables

if __name__ == "__main__":
    create_tables()
    print("Database tables created successfully.")
