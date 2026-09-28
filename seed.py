from app.database import SessionLocal, create_tables
from app.models import Student

create_tables()

sample_students = [
    Student(name="Ravi Kumar", age=21, gender="Male", course="BCA", email="ravi@example.com"),
    Student(name="Sindhu Rao", age=20, gender="Female", course="BCA", email="sindhu@example.com"),
    Student(name="Arun Kumar", age=22, gender="Male", course="BSc", email="arun@example.com"),
    Student(name="Seetha Devi", age=21, gender="Female", course="BCA", email="seetha@example.com"),
]

with SessionLocal() as db:
    if db.query(Student).count() == 0:
        db.add_all(sample_students)
        db.commit()
        print("Sample students inserted.")
    else:
        print("Database already contains students.")
