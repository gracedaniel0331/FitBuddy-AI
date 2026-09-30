from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.routes import router
from app.database import init_db


app = FastAPI(
    title="FitBuddy – AI Fitness Plan Generator",
    description="AI-assisted 7-day fitness planning with Gemini, FastAPI, Jinja2 and SQLite.",
    version="1.0.0",
)


app.mount(
    "/static",
    StaticFiles(directory="static"),
    name="static",
)


app.include_router(router)


@app.on_event("startup")
def startup_event():
    init_db()