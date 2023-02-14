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
    def __init__(self, GradeMain: c_GradeMain,uI: c_termianlUserInterface, jsonFilename="Lab5.json"):
        self.uI = uI
        self.gradeMain = GradeMain
        self.m_initalizeJson(jsonFilename)
        self.f_gradeQuickSortExe = self.m_compileTestingExe(
            "testQuickSort", "testQuickSort.c")
        self.f_gradeSplitExe = self.m_compileTestingExe(
            "testSplit", "testSplit.c")

    def m_initalizeJson(self, filename):
        with open(filename, "r") as f:
            data = json.load(f)

        try:
            self.dueDate = data['dueDate']
            self.filesReq = data['filesReq']
            zipFile = data["zipFile"]
            if zipFile != None:
                self.zipFile = zipFile
        except Exception as e:
            instructions = [f"Data Required not present in jsonFile", f"{e}"]
            options = [f"Continue"]
            self.uI.m_terminalUserInterface(options, instructions)
            exit(0)

        try:
            self.testStrings = data["testStrings"]
        except Exception as e:
            instructions = [f"Data Required not present in jsonFile", f"{e}"]
            options = [f"Continue"]
            self.uI.m_terminalUserInterface(options, instructions)
            exit(0)

        instructions = [f"Json file {filename} has been initialized"]
        options = ["Continue"]
        self.uI.m_terminalUserInterface(options, instructions)

    def m_gradedReport(self, student: c_Student):
        self.m_showFile(student.s_feedbackFile)
        instructions = [f"Student : {student.s_name}",
                        f"Grade   : {student.f_grade}/100", "Select an option:"]
        options = ["Edit grade.file", "Show grade.file", "Continue"]
        while True:
            selectedData = self.uI.m_terminalUserInterface(
                options, instructions)
            if (selectedData == options[0]):
                self.m_editFile(student.s_feedbackFile)
            elif (selectedData == options[1]):
                self.m_showFile(student.s_feedbackFile)
            elif (selectedData == options[2]):
                break

    def m_grade(self, name):
        student: c_Student = self.gradeMain.d_listOfStudents[name]
        currentWorkingDir = os.getcwd()
        path = os.path.join(os.getcwd(), name)
        # print(f'Changing working directory to {path}')
        os.chdir(path)
        student.ls_filenames = list(range(3))
        self.m_Decompress(student,self.zipFile)
        student.s_initialFeedback += f"-----------------------------------------------------------------------\n"
        student.s_initialFeedback += f"Part-1 Reverse the string\n"
        student.s_initialFeedback += f"-----------------------------------------------------------------------\n"
        self.m_CheckQuestion1(student, 8)
        student.s_feedback += student.s_initialFeedback
        student.s_initialFeedback = ""
        student.s_initialFeedback += f"-----------------------------------------------------------------------\n"
        student.s_initialFeedback += f"Part-2 Reverse the string[*pointers]\n"
        student.s_initialFeedback += f"-----------------------------------------------------------------------\n"
        self.m_CheckQuestion2(student, 8)
        student.s_feedback += student.s_initialFeedback
        student.s_initialFeedback = ""
        student.s_initialFeedback += f"-----------------------------------------------------------------------\n"
        student.s_initialFeedback += f"Part-3 Reading lines from a file\n"
        student.s_initialFeedback += f"-----------------------------------------------------------------------\n"
        self.m_CheckQuestion3(student, 8)
        student.s_feedback += student.s_initialFeedback
        student.s_initialFeedback = ""
        self.m_finalizeGrade(student)
        self.m_createFeedbackFile(student.s_feedbackFile, student.s_feedback)
        self.m_gradedReport(student)
        self.m_createFeedbackFile(student.s_feedbackFile, student.s_feedback)
        print(f'Changing working directory back to {currentWorkingDir}')
        os.chdir(currentWorkingDir)

    def m_testQuestion2(self, student: c_Student, outputFile,pointsPerTest):
        self.m_testQuestion1(student,outputFile,pointsPerTest)

    def m_testQuestion1(self, student: c_Student, outputFile,totalPoints):
        pointsDeduct = 0
        pointsPerTest = int(totalPoints/len(self.testStrings["Question1"]))
        for testString in self.testStrings["Question1"]:
            process = subprocess.getstatusoutput(f"echo {testString} | ./{outputFile}")
            if process[0] != 0:
                student.s_initialFeedback += f" {-totalPoints:<6}Error:{process[1]}\n"
                student.s_initialFeedback += f"-----------------------------------------------------------------------\n"
                return -(totalPoints)
            output = ":".join(process[1].split(":")[2::])
            matcher = difflib.SequenceMatcher(None, output, testString[::-1])
            similarity = matcher.ratio() * 100
            if (similarity < 96):
                pointsDeduct -= (totalPoints/5)
                student.s_initialFeedback += f" {-pointsPerTest:<6}Failed Test String      -> {testString}\n"
                student.s_initialFeedback += f" {'':6}your ouput              -> {output}\n"
                student.s_initialFeedback += f" {'':6}desired output          -> {testString[::-1]}\n"
                student.s_initialFeedback += f" {'':6}Similarity Percent      -> {similarity}\n"
                student.s_initialFeedback += f"-----------------------------------------------------------------------\n"
        if (pointsDeduct == 0):
            student.s_initialFeedback += f"{'':6} All test strings passed\n"
        return pointsDeduct
    
    def m_testQuestion3(self, student: c_Student, outputFile,totalPoints):
        pointsDeduct = 0
        testStrings =self.testStrings[outputFile][1]
        testString = "\n".join(self.testStrings[outputFile][1])
        self.m_createFeedbackFile(self.testStrings[outputFile][0],testString)
        process = subprocess.getstatusoutput(f"./{outputFile}")
        returnCode = process[0]
        returnValue = process[1]
        if returnCode != 0:
            student.s_initialFeedback += f" {-totalPoints:<6}Error:{process[1]}\n"
            student.s_initialFeedback += f"-----------------------------------------------------------------------\n"
            return -totalPoints
        else:
            found=[]
            for testString in testStrings:
                if testString in returnValue:
                    found.append(testString)
            pointsDeduct = len(found)-len(testStrings)
            if (len(found) != 10 ): student.s_initialFeedback += f"{pointsDeduct} Points"
            student.s_initialFeedback += f"{len(found)} items found out of {len(testStrings)}\n"
            student.s_initialFeedback += f"{'':6}Test String:{testStrings}\n"
            student.s_initialFeedback += f"{'':6}Your output:{found}\n"
            student.s_initialFeedback += f"-----------------------------------------------------------------------\n"
        if (pointsDeduct == 0):
            student.s_initialFeedback += f"{'':6} All tests passed\n"
        return pointsDeduct



    def m_CheckQuestion1(self, student: c_Student, totalPoint):
        points = 0
        student.ls_filenames[0] = self._CheckFile_(student, self.filesReq[0], totalPoint)
        if (student.ls_filenames[0] != False):
            output = "Question1"
            proc = ["gcc", student.ls_filenames[0], "-o", output]
            if (self.m_compileCfile(proc)):
                pointDeducted = self.m_testQuestion1(student, output,totalPoint)
                points += pointDeducted
            else:
                points -= 5
                student.s_initialFeedback += f" {-5:<6} Compilation Error: {student.ls_filenames[0]}"
            self.m_regrade(student, proc,proc[-3], [points, totalPoint])
        else:
            student.f_grade -= totalPoint

    def m_CheckQuestion2(self, student: c_Student, totalPoint):
        points = 0
        student.ls_filenames[1] = self._CheckFile_(
            student, self.filesReq[1], totalPoint)
        if (student.ls_filenames[1] != False):
            output = "Question2"
            proc = ["gcc", student.ls_filenames[1], "-o", output]
            if (self.m_compileCfile(proc)):
                instructions = self.m_fileToStringList(
                    student.ls_filenames[1])+[f"Did {student.s_name} use pointers to solve the question?"]
                options = ["Yes", "No"]
                response = self.uI.m_terminalUserInterface(
                    options, instructions)
                if (response == options[0]):
                    pointDeducted = self.m_testQuestion1(student, output,totalPoint)
                    points +=pointDeducted
                else:
                    student.s_initialFeedback += f"{-totalPoint:<6} Did not follow instruction, No pointer used!!\n"
                    student.f_grade -= totalPoint
                    return
            else:
                points -= 5
                student.s_initialFeedback += f" {-5:<6} Compilation Error: {student.ls_filenames[0]}"
            self.m_regrade(student, proc, proc[-3],[points, totalPoint])
        else:
            student.f_grade -= totalPoint
            return
    
    def m_CheckQuestion3(self, student: c_Student, totalPoint):
        points = 0
        student.ls_filenames[2] = self._CheckFile_(student, self.filesReq[2], totalPoint)
        if (student.ls_filenames[0] != False):
            output = "Question3"
            proc = ["gcc", student.ls_filenames[2], "-o", output]
            if (self.m_compileCfile(proc)):
                pointDeducted = self.m_testQuestion3(student, output,totalPoint)
                points += pointDeducted
            else:
                points -= 5
                student.s_initialFeedback += f" {-5:<6} Compilation Error: {student.ls_filenames[0]}"
            self.m_regrade(student, proc,proc[-3], [points, totalPoint])
        else:
            student.f_grade -= totalPoint
            return

            
    def m_processFile(self,fileList:list,i_feedback,question):
        file = f"\n".join([i for i in fileList if i != ""])
        feedback = "\nFeedback:\n"
        Question3 = [
            "exit",
            "putchar",
            "fclose",
            "fopen",
            "FILE*",
        ]
        for function in Question3:
            if question == "question3" and function not in file:
                feedback += f"{'':4}* Function {function}() missing from file\n"
        if question == "question2" and ("char*" not in file or "char *"):
            feedback += f"{'':4}* char* missing from file\n"
        if "return" not in file and "exit" not in file:
            feedback += f"{'':4}* No exit function found\n"

        if i_feedback !=  None:
            i_feedback = f"{'':4}* "+ f"\n{'':4}* ".join(i_feedback)
            return file +feedback + i_feedback
        else:
            return file +feedback
        

    def m_regrade(self, student: c_Student, proc,filename, points):
        exefilename = proc[-1]
        feedback = self.m_fileToStringList(filename) 
        i_feedback = self.uI.m_feedbackForm(feedback + ["Feedback:"])
        instructions = student.s_initialFeedback.splitlines() + [exefilename,
        f"Student : {student.s_name}",
        f"Grade   : {points[1]+points[0]}/{points[1]}", "Select an option:"]
        options = ["Edit File", "Recompile", "Regrade", "Continue"]
        while True:
            selectedData = self.uI.m_terminalUserInterface(options, instructions)
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
                method = f"self.m_test{proc[-1]}(student,{points[1]})"
                exec(method)
            elif (selectedData == options[3]):
                student.f_grade+=points[0]
                student.s_initialFeedback += self.m_processFile(feedback,i_feedback,exefilename)
                student.s_initialFeedback +=f"\n-----------------------------------------------------------------------\n"
                break

    # def m_testQuestion3(self, student: c_Student, testExe, outputFile):
    #     points = 0
    #     process = subprocess.Popen([f"{PATH}/{testExe} ./{outputFile}"], stdout=subprocess.PIPE,
    #                                stderr=subprocess.PIPE, stdin=subprocess.PIPE, shell=True, universal_newlines=True)
    #     output, _ = process.communicate()
    #     output = list(filter(None, output.split('\n')))
    #     if "Caught Segmentation Fault" in output:
    #         student.s_initialFeedback += f" {-5:<3}Caught Segmentation Fault: Function implementation is wrong\n"
    #         student.s_initialFeedback += f"-----------------------------------------------------------------------\n"
    #         points -= 5
    #         return points
    #     dict = {}
    #     testStrings = self.testStrings["Question3"]
    #     if len(output) >= 1:
    #         for dictIter in output:
    #             dict.update((json.loads(json.loads(json.dumps(dictIter)))))
    #             points -= 1
    #         for key, value in dict.items():
    #             student.s_initialFeedback += f" {-1:<3}Failed Test String      -> {testStrings[key][0]}\n"
    #             student.s_initialFeedback += f" {'':3}your ouput              -> {value}\n"
    #             student.s_initialFeedback += f" {'':3}desired output          -> {testStrings[key][1]}\n"
    #             student.s_initialFeedback += f"-----------------------------------------------------------------------\n"
    #     else:
    #         student.s_initialFeedback += f"{'':6}All Test Strings Passed\n"
    #         student.s_initialFeedback += f"-----------------------------------------------------------------------\n"

    # def m_CheckQuestion3(self, student: c_Student, totalPoint):
    #     points = 0
    #     student.ls_filenames[2] = self._CheckFile_(
    #         student, self.filesReq[2], totalPoint)
    #     if (student.ls_filenames[2] != False):
    #         output = "Question3.so"
    #         proc = ["gcc", student.ls_filenames[2],"-shared","-o", output]
    #         if (self.m_compileCfile(proc)):
    #             student.s_initialFeedback += f"Testing QuickSort Function\n"
    #             self.m_testQuestion3(student, self.f_gradeQuickSortExe, output)
    #             student.s_initialFeedback += f"Testing Split Function\n"
    #             self.m_testQuestion3(student, self.f_gradeSplitExe, output)
    #         else:
    #             points -= 5
    #             student.s_initialFeedback += f" {-5:<3} Compilation Error: {student.ls_filenames[0]}"
    #         self.m_regrade(student, proc,proc[-4], [points, totalPoint])
    #     else:
    #         student.f_grade -= totalPoint

    
    #     return points