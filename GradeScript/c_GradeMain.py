import os
from c_Student import c_Student
from tabulate import tabulate


class c_GradeMain:
    def __init__(self,dueDate,Grade=100, grader="Satwik Shresth"):
        self.f_grade: float = Grade
        self.s_grader: str = grader
        self.d_listOfStudents: dict = self.m_StudentsDict(dueDate)
        self.d_listOfStudentsGraded: dict = dict()
        self.s_tabFileName = "grades.tab"

    def m_StudentsDict(self,dueDate) -> dict[str,c_Student]:
        dict = {}
        for name in os.listdir("."):
            if os.path.isdir(os.path.join(".", name)):
                dict[name] = c_Student(name,duedate=dueDate)
        return dict

    def m_getStudent(self, name) -> c_Student:
        return self.d_listOfStudents[name]

    def m_tabulateGrades(self) -> str:
        table = [{'Name': name, 'Grades': grades} for name, grades in self.d_listOfStudentsGraded.items()]
        tabulatedData = tabulate(table, headers='keys')
        self.m_CreateFile(tabulatedData)
        return tabulatedData
        
    def m_CreateFile(self,data):
        with open(self.s_tabFileName, 'w') as file:
            file.write(data)
    

    def m_DecompressAll(self,filename):
        for name,student in self.d_listOfStudents.values():
            currentWorkingDir = os.getcwd()
            os.chdir(os.path.join(currentWorkingDir,name))
            student.m_Decompress(filename)
            os.chdir(currentWorkingDir)

            
