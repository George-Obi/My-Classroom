from fastapi import FastAPI
from class_register import ClassRegister
from pydantic import BaseModel
from student import Student


app= FastAPI()

register= ClassRegister('js1','Mrs Juliana',2)

@app.get("/")
def home():
    return {"message":"My Classroom API"}

@app.get("/students")
def get_students():
    return {'students':[{'Name':student.student_name,'ID':student.student_id}for student in register.students]}

class StudentInput(BaseModel):
    name: str
    student_id: str

class AttendanceInput(BaseModel):
    student_id: str
    day: str
    status: str

class ResultInput(BaseModel):
    student_id: str
    subject: str
    score: float

@app.post("/students")
def add_student(student_input: StudentInput):
    student= Student(student_input.name, student_input.student_id)
    register.add_student(student)
    return {'Message':f'{student_input.name} added successfully!'}

@app.post("/attendance")
def mark_attendance(data: AttendanceInput):
    student= next((s for s in register.students if s.student_id == data.student_id), None)
    if not student:
        return {'Error':'Student not found!'}
    if data.day not in ['Monday','Tuesday','Wednesday','Thursday','Friday']:
        return {'Error':'Invalid day!'}
    if data.status.upper() not in ['P','A']:
        return {'Error':'Invalid input! Enter P or A'}
    if data.day not in register.attendance:
        register.attendance[data.day]= {}
    register.attendance[data.day][student.student_name] = 'Present' if data.status == 'P' else 'Absent'
    return {'Message':f'{student.student_name} has been marked {register.attendance[data.day][student.student_name]} for {data.day}'}

@app.get("/students/{student_id}/absences")
def get_absences(student_id: str):
    student= next((s for s in register.students if student_id == s.student_id), None)
    if not student:
        return {'Error': 'Student not found!'}
    count= 0
    for day in register.attendance:
        if register.attendance[day].get(student.student_name) == 'Absent':
            count += 1
    return {'Student': student.student_name, 'Absences': count}

@app.post("/results")
def add_result(data: ResultInput):
    student= next((s for s in register.students if s.student_id == data.student_id), None)
    if not student:
        return {'Error':'Student not found'}
    student.add_result(data.subject, data.score)
    return {'message':f'Result for {student.student_name} added', 'subject': data.subject}

@app.get("/results/ranked")
def rank_students():
    if not register.students:
        return {'Error':'No student in register'}
    ranked= sorted(register.students, key=lambda s: sum(s.result.values()) if s.result else 0, reverse= True)
    return {'ranked students': [{'rank': i+1, 'name': s.student_name, 'total': sum(s.result.values())} for i, s in enumerate(ranked)]}

@app.get("/prefect")
def get_prefect():
    if not register.students:
        return {'Error':'No student exist'}
    prefect= register.select_prefect()
    return {'Prefect': prefect.student_name, 'id': prefect.student_id}