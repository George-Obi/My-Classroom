class Student:
    PASS_MARK= 45
    '''Initializes a new Student Object taking name and student_id as parameters. '''
    def __init__(self, name, student_id):
        self.student_name= name
        self.student_id= student_id
        self.result= {}
        print(f'New student created - {self.student_name}: {self.student_id}')

    def add_result(self, subject:str, score: float):
          '''Takes a subject and its respective score, 
          stores in the student result for further computation'''
          if isinstance(subject, str)  and isinstance(score, (int|float)):
                self.result[subject]= score
          else:
                 raise TypeError('Subject must be a string, Score must be a number!')
           
          print(self.result)
          return self.result

    def get_average(self):
         '''Returns a student average catching potential ZeroDivisionError'''
         sum_of_scores= sum(self.result.values())
         count_subjects= len(self.result)
         try:
              a= sum_of_scores/count_subjects
              print(f'{self.student_name} average: {a:.2f}')
              return a
         except ZeroDivisionError:
              print('Empty result record')
              return 0
         
    def get_grade(self):
         '''Returns a students grade'''
         score= self.get_average()
         if score >= 80:
              return 'A'
         elif score >=65:
              return 'B'
         elif score >= 50:
              return 'C'
         elif score >= 45:
              return 'D'
         else:
              return 'F'

    def is_passing(self):
     '''Checks if a student is passing, using the base pass mark defined as a class constant.'''   
     return self.get_average() >= self.PASS_MARK

    
    def __str__(self):
        '''Human readable info on Student object. Returns student name and ID.'''
        return (f'{self.student_name}, Student ID: {self.student_id}')

    def __repr__(self):
         '''A more technical info on Student object'''
         return f'{self.__class__.__qualname__}: {self.student_name} reg no: {self.student_id}'
