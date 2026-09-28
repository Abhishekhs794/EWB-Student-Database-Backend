from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.database import get_db
from app import crud
from app.schemas import ChatRequest, ChatResponse, StudentCreate, StudentResponse, StudentUpdate
from app.graph import run_chat

router = APIRouter()

@router.post("/students", response_model=StudentResponse, status_code=201)
def create_student(data: StudentCreate, db: Session = Depends(get_db)):
    try:
        return crud.create_student(db, data)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="Email already exists.")

@router.get("/students", response_model=list[StudentResponse])
def read_students(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    db: Session = Depends(get_db),
):
    return crud.get_students(db, skip, limit)

@router.get("/students/{student_id}", response_model=StudentResponse)
def read_student(student_id: int, db: Session = Depends(get_db)):
    student = crud.get_student(db, student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found.")
    return student

@router.put("/students/{student_id}", response_model=StudentResponse)
def update_student(student_id: int, data: StudentUpdate, db: Session = Depends(get_db)):
    student = crud.get_student(db, student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found.")
    try:
        return crud.update_student(db, student, data)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="Email already exists.")

@router.delete("/students/{student_id}")
def delete_student(student_id: int, db: Session = Depends(get_db)):
    student = crud.get_student(db, student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found.")
    crud.delete_student(db, student)
    return {"message": "Student deleted successfully."}

@router.post("/chat", response_model=ChatResponse)
def chat(data: ChatRequest, db: Session = Depends(get_db)):
    try:
        return run_chat(data.message, db)
    except RuntimeError as exc:
        raise HTTPException(status_code=503, detail=str(exc))
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Chatbot error: {exc}")
