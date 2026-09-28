# EWB Student Database Application System - Backend

## Requirements implemented
- Modular backend architecture
- FastAPI REST APIs
- SQLite database
- CRUD operations
- Swagger documentation
- Gemini API integration
- LangGraph chatbot workflow
- Chatbot interaction with student database
- `.env` configuration
- Linux/systemd deployment-ready

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

Put your Gemini API key in `.env`.

Run sample data:

```bash
python seed.py
```

Start the backend:

```bash
uvicorn app.main:app --reload
```

Swagger:
`http://127.0.0.1:8000/docs`

## API endpoints

- POST `/api/students`
- GET `/api/students`
- GET `/api/students/{student_id}`
- PUT `/api/students/{student_id}`
- DELETE `/api/students/{student_id}`
- POST `/api/chat`

## Chat examples

- How many students are there?
- How many male and female students are there?
- How many BCA students are there?
- Tell me about Ravi Kumar.
- List all students.

## Architecture

```text
User
 |
 v
FastAPI /api/chat
 |
 v
LangGraph
 |
 v
Gemini intent classification
 |
 v
Safe predefined database operation
 |
 v
SQLite
 |
 v
Answer
```

The LLM is not allowed to execute arbitrary SQL. It selects a restricted intent,
and the application performs the corresponding database operation.

## Systemd

After testing, edit `systemd/ewb-student.service` with your actual Linux username
and project path, then use:

```bash
sudo cp systemd/ewb-student.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable ewb-student.service
sudo systemctl start ewb-student.service
sudo systemctl status ewb-student.service
```

Logs:

```bash
journalctl -u ewb-student.service -f
```
