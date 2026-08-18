import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent.parent


class Settings:
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./smartmed_companion.db")
    UPLOAD_DIR: str = os.getenv("UPLOAD_DIR", str(BASE_DIR / "uploads" / "prescriptions"))
    MAX_UPLOAD_SIZE: int = int(os.getenv("MAX_UPLOAD_SIZE", "10485760"))
    OCR_LANGUAGE: str = os.getenv("OCR_LANGUAGE", "eng")
    DRUG_API_URL: str = os.getenv("DRUG_API_URL", "")
    DRUG_API_KEY: str = os.getenv("DRUG_API_KEY", "")


settings = Settings()
