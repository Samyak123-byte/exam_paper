import os
from pathlib import Path

from dotenv import load_dotenv


# Project root directory
BASE_DIR = Path(__file__).resolve().parent

# Load .env file
load_dotenv(BASE_DIR / ".env")


class Config:

    # Flask secret key
    SECRET_KEY = os.getenv(
        "SECRET_KEY",
        "ai-osm-development-secret-key"
    )

    # Database
    DATABASE = str(
        BASE_DIR / "database" / "osm.db"
    )

    # Answer sheet uploads
    UPLOAD_FOLDER = str(
        BASE_DIR / "uploads" / "answer_sheets"
    )

    # Question paper uploads
    QUESTION_FOLDER = str(
        BASE_DIR / "uploads" / "question_papers"
    )

    # Output folder
    OUTPUT_FOLDER = str(
        BASE_DIR / "outputs"
    )

    # Maximum upload size = 20 MB
    MAX_CONTENT_LENGTH = 20 * 1024 * 1024

    # Allowed file extensions
    ALLOWED_EXTENSIONS = {
        "png",
        "jpg",
        "jpeg",
        "pdf"
    }