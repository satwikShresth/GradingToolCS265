import os
from c_Student import c_Student


class c_GradeMain:
    def __init__(self, Grade=100, grader="Satwik Shresth"):
        self.f_grade:float = Grade
        self.s_grader:str = grader
        self.d_listOfStudents:dict = self.m_StudentsDict()
        self.ss_listOfStudentsGraded:set = set()

    def m_StudentsDict(self):
        dict = {}
        for name in os.listdir("."):
            if os.path.isdir(os.path.join(".", name)):
                dict[name] = c_Student(name)
        return dict

    def m_getStudent(self, name):
        return self.d_listOfStudents[name]
