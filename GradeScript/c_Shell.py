from c_GradeMain import c_GradeMain
from c_DirOrganizer import c_DirOrganizer
from c_AssignmentTrack import c_AssignmentTrack
from c_Mail import c_Mail
from c_Student import c_Student
from c_TerminalUserInterface import c_termianlUserInterface
# from c_CodeChecker import c_CodeChecker
from tabulate import tabulate
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
        assignment: c_AssignmentTrack = c_AssignmentTrack(self.o_uI,self.assignmentToGrade,self.data)
        self.o_grade = assignment.m_initalizer()
        c_DirOrganizer()
        self.o_gradeMain: c_GradeMain = c_GradeMain(self.o_uI,self.assignmentName)
        # self.codeChecker = c_CodeChecker(self.o_gradeMain)
        self.mail: c_Mail = c_Mail(self.o_gradeMain)
        self.m_loadProgress()
        self.i_assignmentsToGrade: int = len(self.o_gradeMain.d_listOfStudents)
        self.m_menu()




    def m_fileToStringList(self, filename):
        try:
            with open(filename, "r") as file:
                fileContents = [line for line in file.readlines() if line.strip()]
            return fileContents
        except Exception as e:
            instructions = [f"Error:", f"{e}"]
            options = [f"Continue"]
            self.o_uI.m_terminalUserInterface(options, instructions)

    def m_initalizeJson(self, filename):
        currentWorkingDir = os.getcwd()
        self.path = filename
        if os.path.isdir(filename):
            os.chdir(filename)
            while (1):
                display = filename.split("/")[-1]
                instructions = [f"Select a file in {display}:"]
                options = [file for file in os.listdir(filename) if os.path.isfile(file) and file.endswith("json")]
                selectedData = self.o_uI.m_terminalUserInterface(options, instructions)
                if (selectedData == "q"):
                    break
                else:
                    instruction = self.m_fileToStringList(
                        selectedData)+[f"Is {selectedData} Correct?"]
                    option = ["Yes", "No"]
                    response = self.o_uI.m_terminalUserInterface(
                        option, instruction)
                    if (response == option[0]):
                        filename = selectedData
                        break
        else:
            self.path ="/".join((filename.split("/"))[:-1])
            
        
        try:
            with open(filename, "r") as f:
                data = json.load(f)
        except Exception as e:
            instructions = [f"Cannot Open file", f"{e}"]
            options = [f"Continue"]
            self.o_uI.m_terminalUserInterface(options, instructions)
            return False
        
        try:
            self.assignmentName = data["assignmentName"]
            self.dueDate = data['dueDate']
            self.filesReq = data['filesReq']
            zipFile = data["zipFile"]
            if zipFile != None:
                self.zipFile = zipFile
        except Exception as e:
            instructions = [f"Data Required not present in jsonFile", f"{e}"]
            options = [f"Continue"]
            self.o_uI.m_terminalUserInterface(options, instructions)
            return False
        
        os.chdir(currentWorkingDir)
        filename = filename.split("/")[-1]
        instructions = [f"Json file {filename} has been initialized"]
        options = ["Continue"]
        self.o_uI.m_terminalUserInterface(options, instructions)
        return data
        
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    def m_initalizer(self)->bool:
        # Pre-Req
        self.currentWorkingDir = os.getcwd()
        # os.chdir(".//TA-CS265-1")

        while True:
            self.data = self.m_initalizeJson(self.o_uI._selectDirectory_())
            if self.data:
                break

        os.chdir(self.path)

        # Enter Shell

        self.assignmentToGrade = self.data["assignmentName"]
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

    def m_gradeStudent(self, name):
        currentWorkingDir = os.getcwd()
        path = os.path.join(os.getcwd(), name)
        student:c_Student= self.o_gradeMain.d_listOfStudents[name]
        if name in self.o_gradeMain.d_listOfStudentsGraded:
            status = self.o_gradeMain.d_listOfStudentsGraded[name]
        else:
            status = "Needs Grading"
        instructions = [f"Student :{student.s_fullname}", f"Status: {status}",
                        "Select an option:"]
        while True:
            if status == "Needs Grading":
                options = [f"Grade {name}","Exit"]
            else:
                options = [f"Grade {name}","Edit grade.file", "Show grade.file","Exit"]
            selectedData = self.o_uI.m_terminalUserInterface(options, instructions)
            if (selectedData == options[0]):
                
                self.o_grade.m_grade(student)
                self.o_gradeMain.d_listOfStudentsGraded[name]= self.o_gradeMain.m_getStudent(name).f_grade
                self.m_saveProgress()
            elif len(options)>2 and (selectedData == options[1]):
                os.chdir(path)
                student.m_editFile()
                os.chdir(currentWorkingDir)
            elif len(options)>2 and (selectedData == options[2]):
                os.chdir(path)
                student.m_showFile()
                os.chdir(currentWorkingDir)
            elif (selectedData == options[-1]):
                os.chdir(path)
                student.m_registerGrade()
                os.chdir(currentWorkingDir)
                print(f"Back to Menu")
                break
        
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
            self.o_gradeMain.m_saveProfile(name)
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
        options = ["Start Grading","Students","Mail Grades", "Tabulate Grades","Tabulate Runtime Record", "EXIT"]
        while True:
            selectedData = self.o_uI.m_terminalUserInterface(
                options, instructions)
            if (selectedData == options[0]):
                self.m_shellStruct()
            elif (selectedData == options[1]):
                self.m_gradeStudent(
                    self.o_uI.m_selectStudents(self.o_gradeMain.d_listOfStudents,self.o_gradeMain.d_listOfStudentsGraded))
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
                pass
                # self.codeChecker.m_generateReport()
                # self.codeChecker.customCheck()
            elif (selectedData == options[5]):
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