from sqlalchemy import Column, String, Float
from database import Base
import json

class Student(Base):
    __tablename__= "students"

    student_id = Column(String, primary_key= True, index= True)
    student_name = Column(String, nullable= False)
    result = Column(String, default= "{}")

    def set_result(self, result_dict):
        self.result= json.dumps(result_dict)

    def get_result(self):
        return json.loads(self.result)

class Attendance(Base):
    __tablename__= "attendance"

    student_id = Column(String, primary_key=True, index= True)
    day = Column(String, nullable=False)
    student_name = Column(String, nullable= False)
    status= Column(String, nullable=False)