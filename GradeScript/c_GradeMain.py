from myLibs import os, parser, re, zipfile,PATH,c_Student


class c_GradeMain:
    def __init__(self,totalPoints=100):
        self.totalPoints=totalPoints
        self.listOfStudents= self.m_StudentsDict()
        self.feedback={}

    def m_StudentsDict(self):
        dict={}
        for name in os.listdir("."):
            if os.path.isdir(os.path.join(".", name)):
                dict[name]=c_Student(name)
        return dict

    def m_getStudent(self,name):
        return self.listOfStudents[name]