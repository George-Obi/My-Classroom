from random import choices
from student import Student
class ClassRegister:

     num_of_students= 0

     def __init__(self, class_grade):
          '''Initializes a new instance of ClassRegister'''
          self.class_teacher= input('Enter name of form teacher in full: ')
          self.students= []
          self.grade= class_grade
          self.attendance= {}
          self.class_prefect= None

     def add_student(self,student):
          '''Adds a new student to an existing grade(class)'''
          if isinstance(student, Student):
               self.students.append(student)
               self.num_of_students += 1
               return self.students

     

     def class_info(self):
          '''Returns classroom information. Form teacher, Students in a class and total number of students'''
          print(f'INFORMATION ON {self.grade} class\n')
          print(f'Form Teacher: {self.class_teacher}')

          class_list= (f'Students -- {self.students}\n Total number of students in class: {self.num_of_students} students')
          print(class_list)
          return class_list
     

     def compute_subjectscores(self):
          '''Computes and stores subject scores for each student in a dictionary'''
          self.num_of_subjects= int(input('How many subjects do your students offer? '))
          for i in range(self.num_of_subjects):
               subject= input(f'Enter subject {i+1}: ')
               for student in self.students:
                    print(f'Entering results for {student.student_name}')
                    score= float(input('Enter score: '))
                    student.add_result(subject, score)
               
     def count_absences(self, student: Student):
          '''Returns count of student absences provided from the class attendance'''
          count= 0
          for day in self.attendance:
               if self.attendance[day][student.student_name] == 'Absent':
                    count += 1
          return count

     def mark_attendance(self):
          '''Takes class attendance and stores in a dictionary'''
          week_day= input('Enter day of the week(e.g Monday, Tuesday....) ')
          daily_record= {}
          students= sorted(self.students, key=lambda student:student.student_name.lower())
          for student in students:
               map_attendance= {
                    'P':'Present',
                    'A':'Absent'
               }
               while True:
                    mark= input(f'{student.student_name} Present/Absent? Enter P/A: ').upper().strip()
                    if mark not in ['P','A']:
                         print('Invalid input! Enter P/A')
                    else:
                         daily_record[student.student_name]= map_attendance[mark]
                         break
          self.attendance[week_day]= daily_record
          return self.attendance



     def rank_students(self):
          '''Ranks students in a class by performance using average '''
          lst= sorted(self.students, key= lambda student: student.get_average(), reverse= True)
          ranked= []
          for position, student in enumerate(lst, start=1):
               ranked.append(f'{student} - {position}')
          for student in ranked:
               print(student)
          return ranked


     def sort_by_name(self):
          '''Sorts student by name alphabetically'''
          lst= (sorted(self.students, key= lambda student: student.student_name.lower()))
          ranked= []
          for position, student in enumerate(lst, start= 1):
               ranked.append(f'{position}. {student.student_name}')
          for student in ranked:
               print(student)
          return ranked
               

     def select_prefect(self):
          '''Randomly selects one prefect using absence as a parameter'''
          candidates= {}
          for student in self.students:
               if student == self.class_prefect:
                    continue
               absences= self.count_absences(student)
               if absences <=1:
                    candidates[student] = 10
               elif absences == 2:
                    candidates[student] = 5
               else:
                    candidates[student] = 0
          self.class_prefect= choices(list(candidates.keys()), weights=list(candidates.values()),k=1)[0]
          print(f'New Prefect - {self.class_prefect}')
          return self.class_prefect
     

     def __str__(self):
          '''Human readable info on ClassRegister Object. Returns a grade and its number of students'''
          return f'class: {self.grade}; {self.num_of_students} student(s)'
     
     def __repr__(self):
          '''A more technical info on the ClassRegister object'''
          return f'{self.grade} {self.__class__.__qualname__} Student list: {self.students}'