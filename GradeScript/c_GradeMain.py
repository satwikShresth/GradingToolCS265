import os
from c_Student import c_Student


class c_GradeMain:
    def __init__(self,Grade=100,grader="Satwik Shresth"):
        self.grade=Grade
        self.grader=grader
        self.listOfStudents= self.m_StudentsDict()
        self.listOfStudentsGraded= set()
        self.feedback={}

    def m_StudentsDict(self):
        dict={}
        for name in os.listdir("."):
            if os.path.isdir(os.path.join(".", name)):
                dict[name]=c_Student(name)
        return dict

    def m_getStudent(self,name):
        return self.listOfStudents[name]