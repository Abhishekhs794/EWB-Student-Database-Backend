import json
from google import genai
from google.genai import types
from app.config import GEMINI_API_KEY, GEMINI_MODEL

_client = genai.Client(api_key=GEMINI_API_KEY) if GEMINI_API_KEY else None

SYSTEM_INSTRUCTION = '''
You are the Student Database Assistant.

Convert the user's natural-language question into ONE safe database intent.
Allowed intents:
count_students, gender_count, list_students, search_student, course_count, help

Return ONLY JSON:
{"intent":"...", "value":"..."}

Rules:
- Never invent student information.
- search_student: value is the student's name.
- course_count: value is the course name.
- Use help for questions outside the student database.
'''

def classify_question(question: str) -> dict:
    if _client is None:
        raise RuntimeError("GEMINI_API_KEY is not configured.")

    response = _client.models.generate_content(
        model=GEMINI_MODEL,
        contents=question,
        config=types.GenerateContentConfig(
            system_instruction=SYSTEM_INSTRUCTION,
            temperature=0,
            response_mime_type="application/json",
        ),
    )
    try:
        data = json.loads(response.text)
    except Exception as exc:
        raise RuntimeError("Gemini returned invalid JSON.") from exc

    allowed = {
        "count_students", "gender_count", "list_students",
        "search_student", "course_count", "help"
    }
    intent = data.get("intent")
    if intent not in allowed:
        intent = "help"

    return {"intent": intent, "value": str(data.get("value", "")).strip()}
