from c_GradeMain import c_GradeMain
from c_DirOrganizer import c_DirOrganizer
from c_AssignmentTrack import c_AssignmentTrack
from c_Mail import c_Mail
from c_TerminalUserInterface import c_termianlUserInterface
import os
import json
import curses


class c_Shell():
    def __init__(self):
        self.o_uI = c_termianlUserInterface()
        if (self.m_initalizer() == False):
            print("Couldn't initalize the script")
            exit(0)
        c_DirOrganizer().m_organize()
        self.o_gradeMain: c_GradeMain = c_GradeMain()
        self.mail: c_Mail = c_Mail(self.o_gradeMain)
        self.m_loadProgress()
        self.i_assignmentsToGrade: int = len(self.o_gradeMain.d_listOfStudents)
        assignment: c_AssignmentTrack = c_AssignmentTrack(
            self.o_gradeMain, self.assignmentToGrade)
        self.o_grade = assignment.m_initalizer()
        self.m_menu()

    def m_initalizer(self):
        # Pre-Req
        self.currentWorkingDir = os.getcwd()
        os.chdir("../TA-CS265-1")
        curses.initscr()
        curses.endwin()
        path = self.o_uI._selectDirectory_()
        # print(f'Changing working directory to {path}')
        if path == "q":
            exit(0)
        os.chdir(path)

        # Enter Shell

        self.assignmentToGrade = path.split("/")[-1]
        return True

    def m_loadProgress(self):
        try:
            with open("students.graded", "r") as f:
                self.o_gradeMain.d_listOfStudentsGraded  = json.load(f)
        except:
            self.o_gradeMain.d_listOfStudentsGraded =  {}

    def m_saveProgress(self):
        with open("students.graded", "w+") as f:
            json.dump(self.o_gradeMain.d_listOfStudentsGraded, f)

    def m_gradeHelper(self, name):
        instructions = [f"Assignments graded :{len(self.o_gradeMain.d_listOfStudentsGraded)}", f"Assignments left: {self.i_assignmentsToGrade - len(self.o_gradeMain.d_listOfStudentsGraded)}",
                        "Select an option:"]
        options = [f"Grade {name}", "Skip", "Quit"]
        selectedData = self.o_uI.m_terminalUserInterface(
            options, instructions)
        if (selectedData == options[0]):
            self.o_grade.m_grade(name)
            self.o_gradeMain.d_listOfStudentsGraded[name]= self.o_gradeMain.m_getStudent(name).f_grade
            self.m_saveProgress()
            return False
        elif (selectedData == options[1]):
            print(f"{name} Skiped")
            return False
        elif (selectedData == options[2]):
            print(f"Back to Menu")
            return True

    def m_shellFreshGrade(self):
        self.o_gradeMain.d_listOfStudentsGraded = {}
        self.m_saveProgress()
        for name in self.o_gradeMain.d_listOfStudents.keys():
            if (self.m_gradeHelper(name)):
                break

    def m_shellGrade(self):
        for name in self.o_gradeMain.d_listOfStudents.keys():
            if name not in self.o_gradeMain.d_listOfStudentsGraded:
                if (self.m_gradeHelper(name)):
                    break

    def m_menu(self):
        instructions = [f"Total assignments : {self.i_assignmentsToGrade}",
                        f"Number of assignments graded: {len(self.o_gradeMain.d_listOfStudentsGraded)}",
                        "Select an option:"]
        options = ["Start Grading", "Mail Grades", "Tabulate Grades", "EXIT"]
        while True:
            selectedData = self.o_uI.m_terminalUserInterface(
                options, instructions)
            if (selectedData == options[0]):
                self.m_shellStruct()
            elif (selectedData == options[1]):
                self.mail.m_sendMail(
                    list(self.o_gradeMain.d_listOfStudentsGraded))
            elif (selectedData == options[2]):
                instructions = self.o_gradeMain.m_tabulateGrades()
                instructions = instructions.splitlines()
                options = ["Mail", "Exit"]
                selectedData = self.o_uI.m_terminalUserInterface(options, instructions)
                if (selectedData == options[0]):
                    self.mail.m_sendMail(
                    list(self.o_gradeMain.d_listOfStudentsGraded))
            elif (selectedData == options[3]):
                # Post-Req
                # print(f'Changing working directory back to {currentWorkingDir}')
                os.chdir(self.currentWorkingDir)
                exit(0)
            instructions = [f"Return to Main Menu"]
            options = ["Yes"]
            self.o_uI.m_terminalUserInterface(options, instructions)

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
