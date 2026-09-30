
import os
from pathlib import Path

from dotenv import load_dotenv


BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv(BASE_DIR / ".env")


DATABASE_URL = os.getenv(
    "DATABASE_URL",
    f"sqlite:///{BASE_DIR / 'fitbuddy.db'}"
)


GEMINI_API_KEY = (
    os.getenv("GEMINI_API_KEY")
    or os.getenv("GOOGLE_API_KEY")
)


WORKOUT_MODEL = os.getenv(
    "GEMINI_WORKOUT_MODEL",
    "gemini-2.5-pro"
)


TIP_MODEL = os.getenv(
    "GEMINI_TIP_MODEL",
    "gemini-2.5-flash"
)


DEMO_MODE = os.getenv(
    "DEMO_MODE",
    "true"
).lower() in {
    "1",
    "true",
    "yes",
    "on"
}


ADMIN_PASSWORD = os.getenv(
    "ADMIN_PASSWORD",
    "change-me"
)


SESSION_SECRET = os.getenv(
    "SESSION_SECRET",
    "fitbuddy-local-secret"
)
