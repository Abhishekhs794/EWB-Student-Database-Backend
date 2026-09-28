from contextlib import asynccontextmanager
from fastapi import FastAPI

from app.database import create_tables
from app.routes import router

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_tables()
    yield

app = FastAPI(
    title="EWB Student Database Management System",
    description="FastAPI + SQLite CRUD + Gemini + LangGraph chatbot",
    version="1.0.0",
)

app.include_router(router, prefix="/api")

@app.get("/")
def root():
    return {
        "project": "Student Database Application System - Backend",
        "status": "running",
        "docs": "/docs",
    }

@app.get("/health")
def health():
    return {"status": "healthy"}
