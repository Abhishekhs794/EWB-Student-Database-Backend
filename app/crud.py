from sqlalchemy import select
from sqlalchemy.orm import Session
from app.models import Student
from app.schemas import StudentCreate, StudentUpdate

def create_student(db: Session, data: StudentCreate):
    student = Student(**data.model_dump())
    db.add(student)
    db.commit()
    db.refresh(student)
    return student

def get_student(db: Session, student_id: int):
    return db.get(Student, student_id)

def get_students(db: Session, skip=0, limit=100):
    return list(db.scalars(select(Student).offset(skip).limit(limit)).all())

def update_student(db: Session, student, data: StudentUpdate):
    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(student, key, value)
    db.commit()
    db.refresh(student)
    return student

def delete_student(db: Session, student):
    db.delete(student)
    db.commit()
