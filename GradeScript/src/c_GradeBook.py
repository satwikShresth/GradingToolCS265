import os,pickle,threading,time
from c_TerminalUserInterface import c_termianlUserInterface
from c_Student import c_Student
from tabulate import tabulate

PROFILE = "/home/ss5278/GradeScript/studentProfiles"

class c_GradeBook:
    def __init__(self,uI:c_termianlUserInterface,assignmentName,Grade=100, grader="Satwik Shresth"):
        self.o_uI = uI
        self.assignmentName = assignmentName
        self.f_grade: float = Grade
        self.s_grader: str = grader
        self.d_listOfStudents:dict[str:c_Student]
        self.m_StudentsDict()
        self.d_listOfStudentsGraded: dict = dict()
        self.s_tabFileName = "grades.tab"

    def m_StudentsDict(self):
        self.d_listOfStudents = {}
        for name in os.listdir("."):
            if os.path.isdir(os.path.join(".", name)) and name != "references":
                self.m_loadProfile(name)
        self.d_listOfStudents = dict(sorted(self.d_listOfStudents.items()))

    def m_getStudent(self, name) -> c_Student:
        return self.d_listOfStudents[name]



    def m_saveProfile(self,name):
        try:
            with open(os.path.join(PROFILE,f"{name}.profile"), "wb+") as f:
                pickle.dump(self.d_listOfStudents[name],f)
        except Exception as e:
            instructions = [f"Error:", f"{e}"]
            options = [f"Continue"]
            self.o_uI.m_terminalUserInterface(options, instructions)
            

    def m_loadProfile(self,name):
        try:
            with open(os.path.join(PROFILE,f"{name}.profile"), "rb") as f:
                self.d_listOfStudents[name] = pickle.load(f)
            self.d_listOfStudents[name].m_loadProfile(self.assignmentName)

        except Exception as e:
            instructions = [f"Error:", f"{name}.profile not found in database","Create new profile ?"]
            options = [f"Continue","Skip"]
            response = self.o_uI.m_terminalUserInterface(options, instructions)
            if response == options[0]:
                self.d_listOfStudents[name] = c_Student(name)
                with open(os.path.join(PROFILE,f"{name}.profile"), "wb+") as f:
                    pickle.dump(self.d_listOfStudents[name],f)
            
    
    def m_createBBFeedbackFile(self):
        keywords = ["Grader:","Part-","Grade:","All test strings passed","Bad file name: ","Feedback:\n"," -> ","Late Submission:","Question","* "]
        bbFeedbackFile = ""
        for name, _ in self.d_listOfStudentsGraded.items():
            bbFeedbackFile += f"--------------------------------{name}---------------------------------------\n"
            with open(os.path.join(".", name,self.m_getStudent(name).s_feedbackFile),"r") as file:
                lines = file.readlines()
            for line in lines:
                for words in keywords:
                    if words in line:
                        if words == "Question" or words == "Part-":
                            bbFeedbackFile += "-----------------------------------\n"
                            bbFeedbackFile += line
                            bbFeedbackFile += "-----------------------------------\n"
                        else:
                            bbFeedbackFile += line
            bbFeedbackFile += f"----------------------------------------------------------------------"+("-"*len(name))+"\n"

        with open("bbLearnFeedback.txt","w+") as file:
            file.write(bbFeedbackFile)



    def m_tabulateGrades(self) -> str:
        table = []
        self.d_listOfStudentsGraded = dict(sorted(self.d_listOfStudentsGraded.items()))
        for name, grades in self.d_listOfStudentsGraded.items():
            table += [{'Name': self.m_getStudent(name).s_fullname, 'Grades': grades} ]
        tabulatedData = tabulate(table, headers='keys')
        self.m_CreateFile(tabulatedData)
        return tabulatedData
    
        
    def m_CreateFile(self,data):
        try:
            with open(self.s_tabFileName, 'w') as file:
                file.write(data)
        except Exception as e:
            instructions = [f"Error:", f"{e}"]
            options = [f"Continue"]
            self.o_uI.m_terminalUserInterface(options, instructions)