from c_GradeMain import c_GradeMain
from c_DirOrganizer import c_DirOrganizer
from c_AssignmentTrack import c_AssignmentTrack
from c_Mail import c_Mail
from c_TerminalUserInterface import c_termianlUserInterface
import os
import json,sys
import curses


class c_Shell():
    def __init__(self,uI:c_termianlUserInterface):
        self.o_uI:c_termianlUserInterface = uI
        if (self.m_initalizer() == False):
            print("Couldn't initalize the script")
            curses.endwin()
            exit(0)
        assignment: c_AssignmentTrack = c_AssignmentTrack(self.o_uI,self.assignmentToGrade)
        self.o_grade = assignment.m_initalizer()
        c_DirOrganizer().m_organize()
        self.o_gradeMain: c_GradeMain = c_GradeMain(self.o_grade.dueDate)
        self.mail: c_Mail = c_Mail(self.o_gradeMain)
        self.m_loadProgress()
        self.i_assignmentsToGrade: int = len(self.o_gradeMain.d_listOfStudents)
        self.m_menu()
        
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    def m_initalizer(self)->bool:
        # Pre-Req
        self.currentWorkingDir = os.getcwd()
#         os.chdir(".//TA-CS265-1")
        path = self.o_uI._selectDirectory_()
        # print(f'Changing working directory to {path}')
        if path == "q":
            curses.endwin()
            exit(0)
        os.chdir(path)

        # Enter Shell

        self.assignmentToGrade = path.split("/")[-1]
        return True
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    def m_loadProgress(self)->None:
        try:
            with open("students.graded", "r") as f:
                self.o_gradeMain.d_listOfStudentsGraded  = json.load(f)
        except:
            self.o_gradeMain.d_listOfStudentsGraded =  {}
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    def m_saveProgress(self):
        try:
            with open("students.graded", "w+") as f:
                json.dump(self.o_gradeMain.d_listOfStudentsGraded, f)
        except Exception as e:
            instructions = [f"Error:", f"{e}"]
            options = [f"Continue"]
            self.o_uI.m_terminalUserInterface(options, instructions)
            sys.exit(0)
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    def m_gradeHelper(self, name):
        instructions = [f"Assignments graded :{len(self.o_gradeMain.d_listOfStudentsGraded)}", f"Assignments left: {self.i_assignmentsToGrade - len(self.o_gradeMain.d_listOfStudentsGraded)}",
                        "Select an option:"]
        options = [f"Grade {name}", "Skip", "Quit"]
        selectedData = self.o_uI.m_terminalUserInterface(
            options, instructions)
        if (selectedData == options[0]):
            student = self.o_gradeMain.d_listOfStudents[name]
            self.o_grade.m_grade(student)
            self.o_gradeMain.d_listOfStudentsGraded[name]= self.o_gradeMain.m_getStudent(name).f_grade
            self.m_saveProgress()
            return False
        elif (selectedData == options[1]):
            print(f"{name} Skiped")
            return False
        elif (selectedData == options[2]):
            print(f"Back to Menu")
            return True
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    def m_shellFreshGrade(self):
        self.o_gradeMain.d_listOfStudentsGraded = {}
        self.m_saveProgress()
        for name in self.o_gradeMain.d_listOfStudents.keys():
            if (self.m_gradeHelper(name)):
                break
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    def m_shellGrade(self):
        for name in self.o_gradeMain.d_listOfStudents.keys():
            if name not in self.o_gradeMain.d_listOfStudentsGraded:
                if (self.m_gradeHelper(name)):
                    break
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    def m_menu(self):
        instructions = [f"Total assignments : {self.i_assignmentsToGrade}",
                        f"Number of assignments graded: {len(self.o_gradeMain.d_listOfStudentsGraded)}",
                        "Select an option:"]
        options = ["Start Grading","Decompress All Files","Mail Grades", "Tabulate Grades", "EXIT"]
        while True:
            selectedData = self.o_uI.m_terminalUserInterface(
                options, instructions)
            if (selectedData == options[0]):
                self.m_shellStruct()
            elif (selectedData == options[1]):
                try:
                    self.o_gradeMain.m_DecompressAll(self.o_grade.zipFile)
                except Exception as e:
                    instructions = [f"Error:", f"{e}"]
                    options = [f"Continue"]
                    self.o_uI.m_terminalUserInterface(options, instructions)
            elif (selectedData == options[2]):
                curses.endwin()
                self.mail.m_sendMail(
                    list(self.o_gradeMain.d_listOfStudentsGraded))
                self.o_uI.screen = curses.initscr()
            elif (selectedData == options[3]):
                instructions2 = self.o_gradeMain.m_tabulateGrades()
                instructions2 = instructions2.splitlines()
                options2 = ["Mail", "Exit"]
                selectedData = self.o_uI.m_terminalUserInterface(options2,instructions2)
                if (selectedData == options[0]):
                    self.mail.m_sendMail(
                    list(self.o_gradeMain.d_listOfStudentsGraded))
            elif (selectedData == options[4]):
                # Post-Req
                # print(f'Changing working directory back to {currentWorkingDir}')
                
                curses.endwin()
                exit(0)
            instructions1 = [f"Returning to Main Menu"]
            options1 = ["Continue"]
            self.o_uI.m_terminalUserInterface(options1, instructions1)
            
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    def m_shellStruct(self):
        assignmentsGraded = len(self.o_gradeMain.d_listOfStudentsGraded)
        instructions = [f"Total assignments : {self.i_assignmentsToGrade}",
                        f"Number of assignments graded: {len(self.o_gradeMain.d_listOfStudentsGraded)}",
                        "Select an option:"]
        options = ["Grade Leftover", "Start Fresh", "EXIT"]
        if (assignmentsGraded != 0):
            while True:
                selectedData = self.o_uI.m_terminalUserInterface(
                    options, instructions)
                if (selectedData == options[0]):
                    self.m_shellGrade()
                elif (selectedData == options[1]):
                    self.m_shellFreshGrade()
                elif (selectedData == options[2]):
                    break
        else:
            self.m_shellFreshGrade()
