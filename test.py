"""A classroom manager software program that handles basic classroom functions 
such as attendance taking, subject score computing, quick student grading,
classroom prefect shuffling and allocation.
This program is built specially in dedication to my dear Mother, A great teacher.
"""
from class_register import ClassRegister
from student import Student

js1= ClassRegister('js1','Mrs Juliana,',2)

#=====================================================================================#
'''STUDENT AND CLASS REGISTER INSTANTIATION'''

George= Student('George Obi', '001')
Rose= Student('Rose Ocha', '002')
Damian= Student('Damian Okon', '003')

Abby= Student('Abigail Vincent', '004')
Miami= Student('Olga Obi', '005')
Ruth= Student('Ruth Obi','006')

Steve= Student('Steve Nwankwo','007')
Habib= Student('Habib Abdul','008')
Ella= Student('Ella Bankole','009')

js1.add_student(Abby)
js1.add_student(Ella)
js1.add_student(Damian)


#======================================================================================#
'''STUDENT AND CLASS REGISTER FUNCTIONS TEST '''

print(f'{Miami.student_name} {Miami.student_id}') #  Outputs Olga Obi 005
print(js1.class_teacher) #  Outputs Mrs Juliana Obi-Njoku

'''Several classroom function tests'''
js1.class_info()
js1.sort_by_name()
js1.mark_attendance()
print(js1.count_absences(Abby))
js1.select_prefect()

#  Store student results and rank the students based on their average
js1.compute_subjectscores() 
js1.rank_students()

#  Some Student object methods and attributes
Ruth.add_result('Electronics',95)
Ruth.add_result('Technical drawing',88)
Ruth.add_result('Further Mathematics', 90)
print(Ruth.is_passing())
print(Ruth.get_average())
print(Ruth.get_grade())

print(Miami)
print(George)
#=======================================================================================#
