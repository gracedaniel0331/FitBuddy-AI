from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.config import ADMIN_PASSWORD, BASE_DIR
from app.database import get_db
from app.models import User, Plan
from app.schemas import UserInput, FeedbackRequest
from app.gemini_generator import generate_workout_gemini
from app.gemini_flash_generator import generate_nutrition_tip_with_flash
from app.updated_plan import update_workout_plan


router = APIRouter()


templates = Jinja2Templates(
    directory=str(BASE_DIR / "templates")
)