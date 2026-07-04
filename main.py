from fastapi import FastAPI, HTTPException, Depends
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
import models, schemas
from database import engine, sessionLocal
import uuid

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = sessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/app")
def serve_frontend():
    return FileResponse('index.html')

@app.get("/")
def home():
    return {"message": "My Classroom API"}

@app.get("/students")
def get_students(db: Session = Depends(get_db)):
    students = db.query(models.Student).all()
    return {'students': [{'Name': s.student_name, 'ID': s.student_id} for s in students]}

@app.post("/students")
def add_student(student_input: schemas.StudentSchema, db: Session = Depends(get_db)):
    existing = db.query(models.Student).filter(models.Student.student_id == student_input.student_id).first()
    if existing:
        raise HTTPException(status_code=400, detail="Student already exists!")
    new_student = models.Student(student_id=student_input.student_id, student_name=student_input.name)
    new_student.set_result({})
    db.add(new_student)
    db.commit()
    db.refresh(new_student)
    return {'Message': f'{student_input.name} added successfully!'}

@app.post("/attendance")
def mark_attendance(data: schemas.AttendanceSchema, db: Session = Depends(get_db)):
    student = db.query(models.Student).filter(models.Student.student_id == data.student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found!")
    if data.day not in ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']:
        raise HTTPException(status_code=400, detail="Invalid day!")
    if data.status.upper() not in ['P', 'A']:
        raise HTTPException(status_code=400, detail="Invalid input! Enter P or A")
    status_text = 'Present' if data.status.upper() == 'P' else 'Absent'
    record_id = f"{data.student_id}_{data.day}"
    existing = db.query(models.Attendance).filter(models.Attendance.id == record_id).first()
    if existing:
        existing.status = status_text
        db.commit()
        return {'Message': f'{student.student_name} attendance updated to {status_text} for {data.day}'}
    attendance = models.Attendance(id=record_id, day=data.day, student_name=student.student_name, status=status_text)
    db.add(attendance)
    db.commit()
    return {'Message': f'{student.student_name} marked {status_text} for {data.day}'}

@app.get("/students/{student_id}/absences")
def get_absences(student_id: str, db: Session = Depends(get_db)):
    student = db.query(models.Student).filter(models.Student.student_id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found!")
    count = db.query(models.Attendance).filter(
        models.Attendance.student_name == student.student_name,
        models.Attendance.status == 'Absent'
    ).count()
    return {'Student': student.student_name, 'Absences': count}

@app.post("/results")
def add_result(data: schemas.ResultSchema, db: Session = Depends(get_db)):
    student = db.query(models.Student).filter(models.Student.student_id == data.student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found!")
    result = student.get_result()
    result[data.subject] = data.score
    student.set_result(result)
    db.commit()
    db.refresh(student)
    return {'message': f'Result for {student.student_name} added', 'subject': data.subject}

@app.get("/results/ranked")
def rank_students(db: Session = Depends(get_db)):
    students = db.query(models.Student).all()
    if not students:
        raise HTTPException(status_code=404, detail="No students in register")
    ranked = sorted(students, key=lambda s: sum(s.get_result().values()) if s.get_result() else 0, reverse=True)
    return {'ranked students': [{'rank': i+1, 'name': s.student_name, 'total': sum(s.get_result().values())} for i, s in enumerate(ranked)]}

@app.get("/prefect")
def get_prefect(db: Session = Depends(get_db)):
    from random import choices
    students = db.query(models.Student).all()
    if not students:
        raise HTTPException(status_code=404, detail="No students exist")
    attendance_data = db.query(models.Attendance).all()
    absence_counts = {}
    for record in attendance_data:
        if record.status == 'Absent':
            absence_counts[record.student_name] = absence_counts.get(record.student_name, 0) + 1
    candidates = {}
    for student in students:
        absences = absence_counts.get(student.student_name, 0)
        if absences <= 1:
            candidates[student] = 10
        elif absences == 2:
            candidates[student] = 5
        else:
            candidates[student] = 0
    prefect = choices(list(candidates.keys()), weights=list(candidates.values()), k=1)[0]
    return {'Prefect': prefect.student_name, 'id': prefect.student_id}