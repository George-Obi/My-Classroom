from pydantic import BaseModel

class StudentSchema(BaseModel):
    name: str
    student_id: str

    class config:
        from_attributes = True

class AttendanceSchema(BaseModel):
    student_id: str
    day: str
    status: str

class ResultSchema(BaseModel):
    student_id: str
    subject: str
    score: float
