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
    def __init__(self, GradeMain: c_GradeMain, filesReq="lab5_1.c lab5_2.c lab5_3.c", zipFile="lab5.zip"):
        self.uI = c_termianlUserInterface()
        self.gradeMain = GradeMain
        self.filesReq = filesReq.split()
        if (zipFile != None):
            self.zipFile = zipFile
        self.gradeQuickSortExe = self.m_compileTestingExe(
            "testQuickSort", "testQuickSort.c")
        self.gradeSplitExe = self.m_compileTestingExe(
            "testSplit", "testSplit.c")
        self.testStringsQ1 = [
            "Go home, relax. Reverse this string.",
            "Can you handle this? Reverse it.",
            "A quick brown fox jumps over the lazy dog. Reverse.",
            "Easy come, easy go. Reverse it now.",
            "Action speaks louder than words. Reverse this.",
            "Too good to be true. Reverse this statement.",
            "All good things come to those who wait. Reverse it.",
            "Practice makes perfect. Reverse this phrase.",
            "Nothing is impossible. Reverse this belief.",
            "Where there's a will, there's a way. Reverse it."
        ]
        self.testStringsQ3 = {
            "1": [[734, 896, 402, 977, 781, 671, 212, 163, 679, 502], [163, 212, 402, 502, 671, 679, 734, 781, 896, 977]],
            "2": [[194, 732, 243, 952, 719, 812, 603, 541, 890, 910], [194, 243, 541, 603, 719, 732, 812, 890, 910, 952]],
            "3": [[367, 991, 784, 546, 310, 165, 886, 969, 807, 527], [165, 310, 367, 527, 546, 784, 807, 886, 969, 991]],
            "4": [[956, 879, 566, 793, 642, 623, 233, 474, 168, 713], [168, 233, 474, 566, 623, 642, 713, 793, 879, 956]],
            "5": [[758, 191, 903, 443, 526, 986, 849, 598, 126, 660], [126, 191, 443, 526, 598, 660, 758, 849, 903, 986]]
        }
        self.funFact = f"\n\nFun Fact: Your assignment is graded and mailed to you using a script.\n{' ':10}It created by all the cool proggramming language, techniques and tools you are learning in this class\n{' ':10}i.e. Bash,C,awk,grep,python,cat"
        self.footer = "\nBest,\nSatwik Shresth\nBSc Computer Science\nCollege of Computing and Informatics\nDrexel University\nPhiladelphia, PA 19104\nsatwik.shresth@drexel.edu\n"

    def m_regrade(self, student: c_Student, proc):
        filename = proc[-1]
        instructions = [f"Student : {student.name}",
                        f"Grade   : {student.grade}",
                        "Select an option:"]
        options = ["Edit File", "Recompile", "Regrade", "Change"]
        while True:
            screen = curses.initscr()
            selectedData = self.uI.m_terminalUserInterface(
                screen, options, instructions)
            curses.endwin()
            if (selectedData == options[0]):
                self.m_editFile(filename)
            elif (selectedData == options[1]):
                output = self.m_compileCfile(proc)
                if (output):
                    print("Compilation Successful")
                    input()
                else:
                    print(output)
                    input()
            elif (selectedData == options[2]):
                break
            elif (selectedData == options[3]):
                self._CheckFile_(student, filename)

    def m_gradedReport(self, student: c_Student):
        self.m_showFile(student.feedbackFile)
        instructions = [f"Student : {student.name}",
                        f"Grade   : {student.grade}", "Select an option:"]
        options = ["Regrade Question 1", "Regrade Question 2",
                   "Regrade Question 3", "Edit grade.file", "Show grade.file", "Continue"]
        while True:
            screen = curses.initscr()
            selectedData = self.uI.m_terminalUserInterface(
                screen, options, instructions)
            curses.endwin()
            if (selectedData == options[0]):
                self.m_regrade(
                    student, ["gcc", "-o", "Question2", student.filenames[0]])
                self.m_CheckQuestion1(student)
            elif (selectedData == options[1]):
                self.m_regrade(
                    student, ["gcc", "-o", "Question2", student.filenames[1]])
                self.m_CheckQuestion2(student)
            elif (selectedData == options[2]):
                self.m_regrade(
                    student, ["gcc", "-shared", "-o", "Question3", student.filenames[2]])
                self.m_CheckQuestion3(student)
            elif (selectedData == options[3]):
                self.m_editFile(student.feedbackFile)
            elif (selectedData == options[4]):
                self.m_showFile(student.feedbackFile)
            elif (selectedData == options[5]):
                break

    def m_grade(self, name):
        student: c_Student = self.gradeMain.listOfStudents[name]
        currentWorkingDir = os.getcwd()
        path = os.path.join(os.getcwd(), name)
        # print(f'Changing working directory to {path}')
        os.chdir(path)
        student.filenames = list(range(3))
        self.m_CheckQuestion1(student)
        self.m_CheckQuestion2(student)
        self.m_CheckQuestion3(student)
        self.m_finalizeGrade(student)
        self.m_createFeedbackFile(
            student.feedbackFile, student.initialFeedback)
        self.m_gradedReport(student)
        student.feedback += student.initialFeedback
        student.feedback += self.funFact
        student.feedback += self.footer
        self.m_createFeedbackFile(student.feedbackFile, student.feedback)
        print(f'Changing working directory back to {currentWorkingDir}')
        os.chdir(currentWorkingDir)

    def m_testExecutableQuestion1(self, student: c_Student, outputFile):
        pointsDeduct = 0
        for testString in self.testStringsQ1:
            process = subprocess.Popen(
                [f"./{outputFile}"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
            output, error = process.communicate(
                input=testString.encode('utf-8'))
            output = output.decode(errors='ignore')
            output = ":".join(output.split(":")[2::])
            matcher = difflib.SequenceMatcher(None, output, testString[::-1])
            similarity = matcher.ratio() * 100
            if (similarity < 96):
                pointsDeduct += .5
                student.initialFeedback += f" {-.5:<6}Failed Test String      -> {testString}\n"
                student.initialFeedback += f" {'':6}your ouput              -> {output}\n"
                student.initialFeedback += f" {'':6}desired output          -> {testString[::-1]}\n"
                student.initialFeedback += f" {'':6}Similarity Percent      -> {similarity}\n"
                student.initialFeedback += f"-----------------------------------------------------------------------\n"
        return pointsDeduct

    def m_testExecutableQuestion3(self, student: c_Student, testExe, outputFile):
        process = subprocess.Popen([f"{PATH}/{testExe} ./{outputFile}"], stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE, stdin=subprocess.PIPE, shell=True, universal_newlines=True)
        output, _ = process.communicate()
        output = list(filter(None, output.split('\n')))
        if "Caught Segmentation Fault" in output:
            student.initialFeedback += f" {-5:<6}Function implementation is wrong\n"
            student.initialFeedback += f"-----------------------------------------------------------------------\n"
            return
        dict = {}
        points = 0
        if len(output) >= 1:
            for dictIter in output:
                dict.update((json.loads(json.loads(json.dumps(dictIter)))))
                student.grade -= 1
            for key, value in dict.items():
                student.initialFeedback += f" {-1:<6}Failed Test String      -> {self.testStringsQ3[key][0]}\n"
                student.initialFeedback += f" {'':6}your ouput              -> {value}\n"
                student.initialFeedback += f" {'':6}desired output          -> {self.testStringsQ3[key][1]}\n"
                student.initialFeedback += f"-----------------------------------------------------------------------\n"

        else:
            student.initialFeedback += f"{'':6}All Test Strings Passed\n"
            student.initialFeedback += f"-----------------------------------------------------------------------\n"

    def m_compilationError(self, student: c_Student, filename, error, outOf):
        student.initialFeedback += f" {-5:<6} Compilation Error: {error}"
        student.grade -= 5

    def m_CheckQuestion1(self, student: c_Student):
        student.initialFeedback += f"-----------------------------------------------------------------------\n"
        student.filenames[0] = self._CheckFile_(student, self.filesReq[0])
        student.initialFeedback += f"\nPart-1 Reverse the string\n"
        if (student.filenames[0] != False):
            output = "Question1"
            notError = self.m_compileCfile(
                ["gcc", student.filenames[0], "-o", output])
            if (notError == True):
                pointDeducted = self.m_testExecutableQuestion1(student, output)
                if (pointDeducted == 0):
                    student.initialFeedback += f"{'':6} All test strings passed\n"
                student.grade -= pointDeducted
            else:
                self.m_compilationError(
                    student, student.filenames[0], notError, 5)

    def m_CheckQuestion2(self, student: c_Student):
        student.initialFeedback += f"\nPart-2 Reverse the string[*pointers]\n"
        student.initialFeedback += f"-----------------------------------------------------------------------\n"
        student.filenames[1] = self._CheckFile_(student, self.filesReq[1])
        if (student.filenames[1] != False):
            output = "Question2"
            notError = self.m_compileCfile(
                ["gcc", "-o", output, student.filenames[1]])
            if (notError == True):
                subprocess.run(["less", f"{student.filenames[1]}"])
                while (1):
                    grade = input("Grade[?/5]: ")
                    if grade.isdigit():
                        grade = int(grade)
                        if grade > 0 and grade < 6:
                            feedback = input("Feedback: ")
                            student.grade += (grade-5)
                            if (grade-5) == 0:
                                student.initialFeedback += f"{' ':6} {feedback}\n"
                            else:
                                student.initialFeedback += f" {(grade-5):<6} {feedback}\n"
                            pointDeducted = self.m_testExecutableQuestion1(
                                student, output)
                            if (pointDeducted == 0):
                                student.initialFeedback += f" {'':6}All test strings passed\n"
                            else:
                                student.grade -= pointDeducted
                            break

                        elif grade == 0:
                            student.initialFeedback += f" {-10:<6} Did not follow the instructions!\n"
                            student.grade -= 10
                            break
            else:
                self.m_compilationError(
                    student, student.filenames[1], notError, 5)

    def m_CheckQuestion3(self, student: c_Student):
        student.initialFeedback += f"\nPart-3 Modifying split function accept 1 array, 2 int* and return int*\n"
        student.initialFeedback += f"-----------------------------------------------------------------------\n"
        student.filenames[2] = self._CheckFile_(student, self.filesReq[2])
        if (student.filenames[2] != False):
            output = "Question3.so"
            notError = self.m_compileCfile(
                ["gcc", "-shared", "-o", output, student.filenames[2]])
            if (notError == True):
                student.initialFeedback += f"Testing QuickSort Function\n"
                self.m_testExecutableQuestion3(
                    student, self.gradeQuickSortExe, output)
                student.initialFeedback += f"Testing Split Function\n"
                self.m_testExecutableQuestion3(
                    student, self.gradeSplitExe, output)
            else:
                self.m_compilationError(
                    student, student.filenames[2], notError, 10)
