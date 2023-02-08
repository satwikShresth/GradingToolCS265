from c_GradeMain import c_GradeMain
from c_DirOrganizer import c_DirOrganizer
from c_AssignmentTrack import c_AssignmentTrack
from c_Mail import c_Mail
from c_TerminalUserInterface import c_termianlUserInterface
import os
import json
import time
import curses


class c_Shell():
    def __init__(self):
        self.uI = c_termianlUserInterface()
        if (self.initalizer() == False):
            print("Couldn't initalize the script")
            exit(0)
        c_DirOrganizer().organize()
        self.gradeMain = c_GradeMain()
        self.mail = c_Mail(self.gradeMain)
        self.loadProgress()
        self.assignmentsToGrade = len(self.gradeMain.listOfStudents)
        assignment = c_AssignmentTrack(self.gradeMain, self.assignmentToGrade)
        self.grade = assignment.initalizer()
        self.m_menu()

    def initalizer(self):
        # Pre-Req
        self.currentWorkingDir = os.getcwd()
        os.chdir("../TA-CS265-1")
        curses.initscr()
        curses.endwin()
        screen = curses.initscr()
        path = self.uI._selectDirectory_(screen)
        curses.endwin()
        # print(f'Changing working directory to {path}')
        if path == "q":
            exit(0)
        os.chdir(path)

        # Enter Shell

        self.assignmentToGrade = path.split("/")[-1]
        return True

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

    def m_gradeHelper(self, name):
        instructions = [f"Assignments graded :{len(self.gradeMain.listOfStudentsGraded)}", f"Assignments left: {self.assignmentsToGrade - len(self.gradeMain.listOfStudentsGraded)}",
                        "Select an option:"]
        options = [f"Grade {name}", "Skip", "Quit"]
        screen = curses.initscr()
        selectedData = self.uI.m_terminalUserInterface(
            screen, options, instructions)
        curses.endwin()
        if (selectedData == options[0]):
            self.grade.m_grade(name)
            self.gradeMain.listOfStudentsGraded.add(name)
            self.saveProgress()
            return False
        elif (selectedData == options[1]):
            print(f"{name} Skiped")
            return False
        elif (selectedData == options[2]):
            print(f"Back to Menu")
            return True

    def m_shellFreshGrade(self):
        self.gradeMain.listOfStudentsGraded = set()
        self.saveProgress()
        for name in self.gradeMain.listOfStudents.keys():
            if (self.m_gradeHelper(name)):
                break

    def m_shellGrade(self):
        for name in self.gradeMain.listOfStudents.keys():
            if name not in self.gradeMain.listOfStudentsGraded:
                if (self.m_gradeHelper(name)):
                    break

    def m_menu(self):
        instructions = [f"Total assignments : {self.assignmentsToGrade}",
                        f"Number of assignments graded: {len(self.gradeMain.listOfStudentsGraded)}",
                        "Select an option:"]
        options = ["Start Grading", "Mail Grades", "Tabulate Grades", "EXIT"]
        while True:
            screen = curses.initscr()
            selectedData = self.uI.m_terminalUserInterface(
                screen, options, instructions)
            curses.endwin()
            if (selectedData == options[0]):
                self.m_shellStruct()
            elif (selectedData == options[1]):
                self.mail.m_sendMail(list(self.gradeMain.listOfStudentsGraded))
            elif (selectedData == options[2]):
                print("Feature under way")
            elif (selectedData == options[3]):
                # Post-Req
                # print(f'Changing working directory back to {currentWorkingDir}')
                os.chdir(self.currentWorkingDir)
                break
            print("returing back to menu..")
            time.sleep(2)

    def m_shellStruct(self):
        assignmentsGraded = len(self.gradeMain.listOfStudentsGraded)
        instructions = [f"Total assignments : {self.assignmentsToGrade}",
                        f"Number of assignments graded: {len(self.gradeMain.listOfStudentsGraded)}",
                        "Select an option:"]
        options = ["Grade Leftover", "Start Fresh", "EXIT"]
        if (assignmentsGraded != 0):
            while True:
                screen = curses.initscr()
                selectedData = self.uI.m_terminalUserInterface(
                    screen, options, instructions)
                curses.endwin()
                if (selectedData == options[0]):
                    self.m_shellGrade()
                elif (selectedData == options[1]):
                    self.m_shellFreshGrade()
                elif (selectedData == options[2]):
                    break
        else:
            self.m_shellFreshGrade()
