from c_GradeMain import c_GradeMain
from c_DirOrganizer import c_DirOrganizer
from c_GradeLab5 import c_GradeLab5
from c_Mail import c_Mail
import os,json


class c_Shell():
    def __init__(self):
        if(self.initalizer()== False):
            print("Couldn't initalize the script")
            exit(0)
        c_DirOrganizer().organize()
        self.gradeMain = c_GradeMain()
        self.mail = c_Mail(self.gradeMain)
        self.loadProgress()
        self.assignmentsToGrade= len(self.gradeMain.listOfStudents)
        self.grade=c_GradeLab5(self.gradeMain)
        self.m_menu()

    def initalizer(self):
        print(f"Current Working Directory: {os.getcwd()}")
        print("Assignments available:-")
        for file in os.listdir("."):
            if os.path.isdir(file):
                print(file, end=" ")
        print()
        while(1):
                ipt=input("Which Assignment would you like to grade [q to exit]: ")
                if ipt == "q":
                    return False
                elif os.path.isdir(ipt):
                    os.chdir(ipt)
                    self.assignmentGraded = ipt
                    return True
                else:
                    print("Try Again!!")
    
    def loadProgress(self):
        try:
            with open("students.graded", "r") as f:
                data = json.load(f)
            self.gradeMain.listOfStudentsGraded = set(data)
        except:
            self.gradeMain.listOfStudentsGraded = set()

    def saveProgress(self):
        with open("students.graded", "w+") as f:
            json.dump(list(self.gradeMain.listOfStudentsGraded), f)

    def _gradeHelper_(self,name,assignmentsGraded):
            userInput = ""
            print(f"Graded : {assignmentsGraded}")
            print(f"Number of assignments left {self.assignmentsToGrade - assignmentsGraded}")
            while True:
                userInput = input(f"Grade {name} [(y)es/(n)o/(q)uit]: ")
                match userInput.lower():
                    case "y":
                        self.grade.m_gradeLab5(name)
                        self.gradeMain.listOfStudentsGraded.add(name)
                        self.saveProgress()
                        break
                    case "n":
                        print("No")
                        break
                    case "q":
                        print("quit")
                        break
                    case _:
                        print("try again")
                        continue
            
            return userInput
                
    
    def m_shellFreshGrade(self):
        self.gradeMain.listOfStudentsGraded =set()
        self.saveProgress()
        assignmentsGraded=len(self.gradeMain.listOfStudentsGraded)
        for name in self.gradeMain.listOfStudents.keys():
            response = self._gradeHelper_(name,assignmentsGraded)
            match response.lower():
                case "y":
                    assignmentsGraded+=1
                case "q":
                    print("quit")
                    break;
            

    def m_shellGrade(self):
        assignmentsGraded=len(self.gradeMain.listOfStudentsGraded)
        for name in self.gradeMain.listOfStudents.keys():
            if name not in self.gradeMain.listOfStudentsGraded:
                response = self._gradeHelper_(name,assignmentsGraded)
                match response.lower():
                    case "y":
                        assignmentsGraded+=1
                    case "q":
                        print("quit")
                        break;


    def m_menu(self):
        while True:
            assignmentsGraded=len(self.gradeMain.listOfStudentsGraded)
            print(f"Number of Students to grade : {self.assignmentsToGrade}")
            print(f"Number of assignments graded: {assignmentsGraded}")
            print(f"------------------------------------------------------------------------------")
            print(f"Options:-")
            print(f"(G)rade   - Start grading students")
            print(f"(M)ail    - All the students there grade")
            print(f"(T)ab     - Tabulate all the grade")
            print(f"(E)xit    - Do nothing")
            userInput = input(f"Enter Action> ")
            match userInput.lower():
                case "g":
                    print(f"------------------------------------------------------------------------------")
                    self.m_shellStruct()
                case "m":
                    print(f"------------------------------------------------------------------------------")
                    self.mail.m_sendMail(list(self.gradeMain.listOfStudentsGraded))
                    print(f"------------------------------------------------------------------------------")
                case "t":
                    print("Feature under way")
                case "e":
                    break
                case _:
                    print("try again")
                    continue



    def m_shellStruct(self):
        assignmentsGraded=len(self.gradeMain.listOfStudentsGraded)
        if (assignmentsGraded !=0):
            while True:
                print(f"------------------------------------------------------------------------------")
                print(f"Number of assignments already graded: {assignmentsGraded} out of {self.assignmentsToGrade}")
                userInput = input("Do you want to start Grading form where you left? [(y)es/(n)o/(q)uit]: ")
                match userInput:
                    case "y":
                        self.m_shellGrade()
                        break
                    case "n":
                        self.m_shellFreshGrade()
                        break
                    case "q":
                        print("quit")
                        break
                    case _:
                        print("try again")
                        continue
        else:
            self.m_shellFreshGrade()
