import curses
import os
import subprocess
import json
import difflib
from c_TerminalUserInterface import c_termianlUserInterface
from c_AssignmentTrack import c_AssignmentTrack
from c_GradeMain import c_GradeMain
from c_Student import c_Student


PATH = "/home/ss5278/GradeScript"


class c_GradeLab5(c_AssignmentTrack):
    def __init__(self, GradeMain: c_GradeMain,jsonFilename="Lab5.json"):
        self.uI = c_termianlUserInterface()
        self.f_gradeMain = GradeMain
        self.m_initalizeJson("Lab5.json")
        self.f_gradeQuickSortExe = self.m_compileTestingExe(
            "testQuickSort", "testQuickSort.c")
        self.f_gradeSplitExe = self.m_compileTestingExe(
            "testSplit", "testSplit.c")


    def m_initalizeJson(self,filename):
        with open(filename, "r") as f:
                data = json.load(f)

        try:
            self.filesReq = data['filesReq']
            zipFile = data["zipFile"]
            if zipFile != None:
                self.zipFile = zipFile
        except Exception as e:
            instructions = [f"Data Required not present in jsonFile",f"{e}"]
            options = [f"Continue"]
            screen = curses.initscr()
            self.uI.m_terminalUserInterface(screen, options, instructions)
            curses.endwin()
            exit(0)

        try:
            self.testStrings = data["testStrings"]
        except Exception as e:
            instructions = [f"Data Required not present in jsonFile",f"{e}"]
            options = [f"Continue"]
            screen = curses.initscr()
            self.uI.m_terminalUserInterface(screen, options, instructions)
            curses.endwin()
            exit(0)

        instructions = [f"Json file {filename} has been initialized"]
        options = ["Continue"]
        screen = curses.initscr()
        self.uI.m_terminalUserInterface(screen, options, instructions)
        curses.endwin()
    





    def m_gradedReport(self,student: c_Student):
        self.m_showFile(student.s_feedbackFile)
        instructions = [f"Student : {student.s_name}",
                        f"Grade   : {student.f_grade}/100", "Select an option:"]
        options = ["Edit grade.file", "Show grade.file", "Continue"]
        while True:
            screen = curses.initscr()
            selectedData = self.uI.m_terminalUserInterface(
                screen, options, instructions)
            curses.endwin()
            if (selectedData == options[0]):
                self.m_editFile(student.s_feedbackFile)
            elif (selectedData == options[1]):
                self.m_showFile(student.s_feedbackFile)
            elif (selectedData == options[2]):
                break

    # def m_gradedReport(self,student: c_Student):
    #     self.m_showFile(student.s_feedbackFile)
    #     instructions = [f"Student : {student.s_name}",
    #                     f"Grade   : {student.f_grade}", "Select an option:"]
    #     options = [f"Regrade file {n}" for n in student.ls_filenames] +["Edit grade.file", "Show grade.file", "Continue"]
    #     while True:
    #         screen = curses.initscr()
    #         selectedData = self.uI.m_terminalUserInterface(
    #             screen, options, instructions)
    #         curses.endwin()
    #         if (selectedData == options[2]):
    #             self.m_regrade(
    #                 student, ["gcc", "-shared", "-o", "Question3", student.ls_filenames[2]])
    #             self.m_CheckQuestion3(student)
    #         elif (selectedData == options[3]):
    #             self.m_editFile(student.s_feedbackFile)
    #         elif (selectedData == options[4]):
    #             self.m_showFile(student.s_feedbackFile)
    #         elif (selectedData == options[5]):
    #             break
    #         else:
    #             selectedData = selectedData.split()[-1]
    #             self.m_regrade(student,["gcc","-o",f"Question{student.ls_filenames.index(selectedData.split()[-1])+1}",selectedData])
    #             method = f"self.m_CheckQuestion{student.ls_filenames.index(selectedData)+1}(student)"
    #             exec(method)

    def m_grade(self, name):
        student: c_Student = self.f_gradeMain.d_listOfStudents[name]
        currentWorkingDir = os.getcwd()
        path = os.path.join(os.getcwd(), name)
        # print(f'Changing working directory to {path}')
        os.chdir(path)
        student.ls_filenames = list(range(3))
        # self.m_Decompress(student)
        student.s_initialFeedback += f"-----------------------------------------------------------------------\n"
        student.s_initialFeedback += f"\nPart-1 Reverse the string\n"
        self.m_CheckQuestion1(student,10,True)
        student.s_initialFeedback += f"\nPart-2 Reverse the string[*pointers]\n"
        student.s_initialFeedback += f"-----------------------------------------------------------------------\n"
        self.m_CheckQuestion2(student,10,True)
        student.s_initialFeedback += f"\nPart-3 Modifying split function accept 1 array, 2 int* and return int*\n"
        student.s_initialFeedback += f"-----------------------------------------------------------------------\n"
        self.m_CheckQuestion3(student,15,True)
        self.m_finalizeGrade(student)
        self.m_createFeedbackFile(
            student.s_feedbackFile, student.s_initialFeedback)
        self.m_gradedReport(student)
        student.s_feedback += student.s_initialFeedback
        self.m_createFeedbackFile(student.s_feedbackFile, student.s_feedback)
        print(f'Changing working directory back to {currentWorkingDir}')
        os.chdir(currentWorkingDir)

    def m_testExecutableQuestion1(self, student: c_Student, outputFile):
        pointsDeduct = 0
        for testString in self.testStrings["Question1"]:
            process = subprocess.Popen(
                [f"./{outputFile}"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
            output, error = process.communicate(
                input=testString.encode('utf-8'))
            output = output.decode(errors='ignore')
            output = ":".join(output.split(":")[2::])
            matcher = difflib.SequenceMatcher(None, output, testString[::-1])
            similarity = matcher.ratio() * 100
            if (similarity < 96):
                pointsDeduct -= .5
                student.s_initialFeedback += f" {-.5:<6}Failed Test String      -> {testString}\n"
                student.s_initialFeedback += f" {'':6}your ouput              -> {output}\n"
                student.s_initialFeedback += f" {'':6}desired output          -> {testString[::-1]}\n"
                student.s_initialFeedback += f" {'':6}Similarity Percent      -> {similarity}\n"
                student.s_initialFeedback += f"-----------------------------------------------------------------------\n"
        return pointsDeduct

    def m_testExecutableQuestion3(self, student: c_Student, testExe, outputFile):
        points=0
        process = subprocess.Popen([f"{PATH}/{testExe} ./{outputFile}"], stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE, stdin=subprocess.PIPE, shell=True, universal_newlines=True)
        output, _ = process.communicate()
        output = list(filter(None, output.split('\n')))
        if "Caught Segmentation Fault" in output:
            student.s_initialFeedback += f" {-5:<6}Function implementation is wrong\n"
            student.s_initialFeedback += f"-----------------------------------------------------------------------\n"
            points-=5
            return points
        dict = {}
        testStrings = self.testStrings["Question3"]
        if len(output) >= 1:
            for dictIter in output:
                dict.update((json.loads(json.loads(json.dumps(dictIter)))))
                points-= 1
            for key, value in dict.items():
                student.s_initialFeedback += f" {-1:<6}Failed Test String      -> {testStrings[key][0]}\n"
                student.s_initialFeedback += f" {'':6}your ouput              -> {value}\n"
                student.s_initialFeedback += f" {'':6}desired output          -> {testStrings[key][1]}\n"
                student.s_initialFeedback += f"-----------------------------------------------------------------------\n"

        else:
            student.s_initialFeedback += f"{'':6}All Test Strings Passed\n"
            student.s_initialFeedback += f"-----------------------------------------------------------------------\n"
        return points

    def m_compilationError(self, student: c_Student,error):
        student.s_initialFeedback += f" {-5:<6} Compilation Error: {error}"
        student.f_grade -= 5

    def m_CheckQuestion1(self, student: c_Student,totalPoint,reGrade):
        points=0
        student.ls_filenames[0] = self._CheckFile_(student, self.filesReq[0],totalPoint)
        if (student.ls_filenames[0] != False):
            output = "Question1"
            proc = ["gcc", student.ls_filenames[0], "-o", output]
            if (self.m_compileCfile(proc)):
                pointDeducted = self.m_testExecutableQuestion1(student, output)
                if (pointDeducted == 0):
                    student.s_initialFeedback += f"{'':6} All test strings passed\n"
                    points-= pointDeducted
            else:
                points -= 5
                self.m_compilationError(student, student.ls_filenames[0])
            if(reGrade):self.m_regrade(student,proc,[points,totalPoint])
        else:
            student.f_grade -= totalPoint

    def m_CheckQuestion2(self, student: c_Student,totalPoint,reGrade):
        points=0
        student.ls_filenames[1] = self._CheckFile_(student, self.filesReq[1],totalPoint)
        if (student.ls_filenames[1] != False):
            output = "Question2"
            proc=["gcc", "-o", output, student.ls_filenames[1]]
            if (self.m_compileCfile(proc)):
                instructions = self.m_fileToStringList(student.ls_filenames[1])+[f"Did {student.s_name} use pointers to solve the question?"]
                options = ["Yes","No"]
                screen = curses.initscr()
                response = self.uI.m_terminalUserInterface(screen, options, instructions)
                curses.endwin()
                if(response == options[0]):
                    pointDeducted = self.m_testExecutableQuestion1(student, output)
                    if(pointDeducted == 0):
                        student.s_initialFeedback += f"{'':6} All test strings passed\n"
                        points-= pointDeducted
                else:
                    student.s_initialFeedback += f"{-totalPoint:<6} Did not follow instruction, No pointer used!!\n"
                    student.f_grade -=totalPoint
                    return
            else:
                points -= 5
                self.m_compilationError(student, student.ls_filenames[1])
            if(reGrade):self.m_regrade(student,proc,[points,totalPoint])
        else:
            student.f_grade -=totalPoint
            return

    def m_CheckQuestion3(self, student: c_Student,totalPoint,reGrade):
        points=0
        student.ls_filenames[2] = self._CheckFile_(student, self.filesReq[2],totalPoint)
        if (student.ls_filenames[2] != False):
            output = "Question3.so"
            proc =["gcc", "-o", output, student.ls_filenames[1]]
            if (self.m_compileCfile(proc)):
                student.s_initialFeedback += f"Testing QuickSort Function\n"
                self.m_testExecutableQuestion3(student, self.f_gradeQuickSortExe, output)
                student.s_initialFeedback += f"Testing Split Function\n"
                self.m_testExecutableQuestion3(student, self.f_gradeSplitExe, output)
            else:
                points -=5
                self.m_compilationError(student, student.ls_filenames[2])
            if(reGrade):self.m_regrade(student,proc,[points,totalPoint])
        else:
            student.f_grade -=totalPoint
