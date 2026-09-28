from typing import TypedDict
from langgraph.graph import StateGraph, START, END
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.chatbot import classify_question
from app.models import Student

class ChatState(TypedDict, total=False):
    question: str
    intent: str
    value: str
    answer: str

def build_graph(db: Session):
    def classify_node(state: ChatState):
        result = classify_question(state["question"])
        return {"intent": result["intent"], "value": result["value"]}

    def database_node(state: ChatState):
        intent = state["intent"]
        value = state.get("value", "")

        if intent == "count_students":
            count = db.scalar(select(func.count(Student.id))) or 0
            answer = f"There are {count} student(s) in the database."

        elif intent == "gender_count":
            rows = db.execute(
                select(Student.gender, func.count(Student.id))
                .group_by(Student.gender)
            ).all()
            answer = (
                "There are no students in the database."
                if not rows
                else "Gender-wise count — " + ", ".join(
                    f"{gender}: {count}" for gender, count in rows
                ) + "."
            )

        elif intent == "course_count":
            if not value:
                answer = "Please provide the course name."
            else:
                count = db.scalar(
                    select(func.count(Student.id))
                    .where(Student.course.ilike(value))
                ) or 0
                answer = f"There are {count} student(s) in the {value} course."

        elif intent == "search_student":
            if not value:
                answer = "Please provide a student name."
            else:
                student = db.scalar(
                    select(Student).where(Student.name.ilike(value))
                )
                answer = (
                    f"Student found: {student.name}, age {student.age}, "
                    f"gender {student.gender}, course {student.course}, "
                    f"email {student.email}."
                    if student else f"No student named {value} was found."
                )

        elif intent == "list_students":
            students = list(db.scalars(select(Student).limit(50)).all())
            answer = (
                "There are no students in the database."
                if not students
                else "Students: " + "; ".join(
                    f"{s.id}. {s.name} ({s.course})" for s in students
                )
            )

        else:
            answer = (
                "I can answer student database questions such as total students, "
                "gender counts, course counts, student details, and student lists."
            )

        return {"answer": answer}

    graph = StateGraph(ChatState)
    graph.add_node("classify", classify_node)
    graph.add_node("database", database_node)
    graph.add_edge(START, "classify")
    graph.add_edge("classify", "database")
    graph.add_edge("database", END)
    return graph.compile()

def run_chat(question: str, db: Session):
    app = build_graph(db)
    result = app.invoke({"question": question})
    return {"answer": result["answer"], "intent": result["intent"]}
