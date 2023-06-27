import os
from dotenv import load_dotenv

load_dotenv()
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+psycopg2://catwatcher_user:catwatcher_pw@192.168.1.157:5432/catwatcher_db",
)
