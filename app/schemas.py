from pydantic import BaseModel, ConfigDict, EmailStr, Field

class StudentBase(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    age: int = Field(ge=1, le=100)
    gender: str = Field(min_length=1, max_length=20)
    course: str = Field(min_length=1, max_length=100)
    email: EmailStr

class StudentCreate(StudentBase):
    pass

class StudentUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=2, max_length=100)
    age: int | None = Field(default=None, ge=1, le=100)
    gender: str | None = Field(default=None, min_length=1, max_length=20)
    course: str | None = Field(default=None, min_length=1, max_length=100)
    email: EmailStr | None = None

class StudentResponse(StudentBase):
    id: int
    model_config = ConfigDict(from_attributes=True)

class ChatRequest(BaseModel):
    message: str = Field(min_length=2, max_length=500)

class ChatResponse(BaseModel):
    answer: str
    intent: str
