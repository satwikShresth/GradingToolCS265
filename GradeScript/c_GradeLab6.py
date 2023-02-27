import os
import subprocess
import json
from c_TerminalUserInterface import c_termianlUserInterface
from c_AssignmentTrack import c_AssignmentTrack
from c_Student import c_Student


PATH = "/home/ss5278/GradeScript"


class c_GradeLab6(c_AssignmentTrack):
    def __init__(self,uI: c_termianlUserInterface, jsonFilename="Lab6.json"):
        self.o_uI = uI
        self.m_initalizeJson(jsonFilename)

    def m_initalizeJson(self, filename):
        try:
            with open(filename, "r") as f:
                data = json.load(f)
        except Exception as e:
            instructions = [f"Cannot Open file", f"{e}"]
            options = [f"Continue"]
            self.o_uI.m_terminalUserInterface(options, instructions)
            exit(0)

        try:
            self.dueDate = data['dueDate']
            self.filesReq = data['filesReq']
            zipFile = data["zipFile"]
            if zipFile != None:
                self.zipFile = zipFile
        except Exception as e:
            instructions = [f"Data Required not present in jsonFile", f"{e}"]
            options = [f"Continue"]
            self.o_uI.m_terminalUserInterface(options, instructions)
            exit(0)

        try:
            self.testStrings = data["testStrings"]
        except Exception as e:
            instructions = [f"Data Required not present in jsonFile", f"{e}"]
            options = [f"Continue"]
            self.o_uI.m_terminalUserInterface(options, instructions)
            exit(0)

        instructions = [f"Json file {filename} has been initialized"]
        options = ["Continue"]
        self.o_uI.m_terminalUserInterface(options, instructions)

    def m_gradedReport(self, student: c_Student):
        self.m_showFile(student.s_feedbackFile)
        instructions = [f"Student : {student.s_name}",
                        f"Grade   : {student.f_grade}/100", "Select an option:"]
        options = ["Edit grade.file", "Show grade.file", "Continue"]
        while True:
            selectedData = self.o_uI.m_terminalUserInterface(
                options, instructions)
            if (selectedData == options[0]):
                self.m_editFile(student.s_feedbackFile)
            elif (selectedData == options[1]):
                self.m_showFile(student.s_feedbackFile)
            elif (selectedData == options[2]):
                break

    def m_grade(self,student:c_Student):
        name = student.s_name
        currentWorkingDir = os.getcwd()
        path = os.path.join(os.getcwd(), name)
        # print(f'Changing working directory to {path}')
        os.chdir(path)
        student.ls_filenames = list(range(1))
        if self.m_Decompress(student,self.zipFile):
            student.s_initialFeedback += f"-----------------------------------------------------------------------\n"
            student.s_initialFeedback += f"Part-1 Reverse the string\n"
            student.s_initialFeedback += f"-----------------------------------------------------------------------\n"
            self.m_CheckQuestion1(student, 5)
            student.s_feedback += student.s_initialFeedback
            student.s_initialFeedback = ""
        else:
            student.s_feedback += f"-----------------------------------------------------------------------\n"
            student.s_feedback += f"No zipFile found\n"
            student.s_feedback += f"-----------------------------------------------------------------------\n"
            student.f_grade = 0
        self.m_finalizeGrade(student)
        self.m_createFeedbackFile(student.s_feedbackFile, student.s_feedback)
        self.m_gradedReport(student)
        self.m_registerGrade(student)
        print(f'Changing working directory back to {currentWorkingDir}')
        os.chdir(currentWorkingDir)


    def m_registerGrade(self,student:c_Student):
        content = self.m_fileToStringList(student.s_feedbackFile)
        for line in content:
            if "Grade:" in line:
                grade = float(line.split("Grade:")[1].strip())
                student.f_grade = grade
            if "Name:" in line:
                student.s_fullname = str(line.split("Name: ")[1].strip())

    def m_testQuestion1(self, student: c_Student, outputFile,totalPoints):
        pointsDeduct = 0
        pointsPerTest = totalPoints
        for testString in self.testStrings["Question1"]:
            test = '\n'.join(testString[0])+"\n"+"\n"
            ans = testString[1]
            try:
                process = subprocess.getstatusoutput(f'printf "{test}" | ./{outputFile} | iconv -f iso-8859-1 -t utf-8//IGNORE')
            except Exception as e:
                student.s_initialFeedback += f" {-totalPoints:<6}Error: {e}\n"
                student.s_initialFeedback += f"-----------------------------------------------------------------------\n"
                return -(totalPoints)
            if process[0] != 0:
                student.s_initialFeedback += f" {-totalPoints:<6}Error:{process[1]}\n"
                student.s_initialFeedback += f"-----------------------------------------------------------------------\n"
                return -(totalPoints)
            output = process[1]
            if (ans not in output):
                pointsDeduct -= pointsPerTest
                student.s_initialFeedback += f" {-pointsPerTest:<6}Failed Test String      -> {testString[0]}\n"
                student.s_initialFeedback += f" {'':6}your ouput              -> {output}\n"
                student.s_initialFeedback += f" {'':6}desired output          -> {ans}\n"
                student.s_initialFeedback += f"-----------------------------------------------------------------------\n"
        if (pointsDeduct == 0):
            student.s_initialFeedback += f"{'':6} All test strings passed\n"
            student.s_initialFeedback += f"-----------------------------------------------------------------------\n"
        return pointsDeduct

    def m_CheckQuestion1(self, student: c_Student, totalPoint):
        points = 0
        student.ls_filenames[0] = self._CheckFile_(student, self.filesReq[0], totalPoint)
        if (student.ls_filenames[0] != False):
            output = "Question1"
            proc = ["gcc", student.ls_filenames[0], "-o", output]
            result = self.m_compileCfile(proc)
            if (result == True):
                pointDeducted = self.m_testQuestion1(student, output,totalPoint)
                points += pointDeducted
            else:
                points -= 5
                student.s_initialFeedback += f" {-5:<6} Compilation Error: {result}"
            self.m_regrade(student, proc,proc[-3], [points, totalPoint])
        else:
            student.f_grade -= totalPoint
            
    def m_processFile(self,fileContentList:list,i_feedback):
        file = f"\n".join([i for i in fileContentList if i != ""])
        i_feedback = "\n"+ f"\n{'':4}* ".join(i_feedback)
        return file + i_feedback
        
    def m_autoCheck(self,student: c_Student,fileContentList,exec):
        fileContent = f"\n".join([i for i in fileContentList if i != ""])
        output=""
        testString = '\n'.join(self.testStrings["Question1"][0][0])+"\n"+"\n"
        try:
            _, output = subprocess.getstatusoutput(f"printf {testString} |valgrind --leak-check=full --show-leak-kinds=all ./{exec}| iconv -f iso-8859-1 -t utf-8//IGNORE")
        except Exception as e:
            student.s_initialFeedback += f"Error while checking memory leak: {e}\n"
        feedback = ["Feedback:"]
        if "All heap blocks were freed -- no leaks are possible" not in output:
            feedback.append(f"-1 Point: Memory leaks detected!")
            student.f_grade -=1

        Question3 = [
            "malloc",
            "free",
        ]
        for function in Question3:
            if exec == "Question3" and function not in fileContent:
                feedback.append(f"Function {function}() missing from file")
        if self.o_uI.m_checkUnreadable(fileContent) == False:
            feedback.append(f"Null character found in file")
        if "return" not in fileContent and "exit" not in fileContent:
            feedback.append(f"No exit function found")

        return feedback
        

        

    def m_regrade(self, student: c_Student, proc,filename, points):
        initalFeedback = student.s_initialFeedback.splitlines()
        exefilename = proc[-1]
        fileContent = self.m_fileToStringList(filename)
        i_feedback = self.m_autoCheck(student,fileContent,exefilename)
        temp = self.o_uI.m_feedbackForm(fileContent + initalFeedback+i_feedback)
        if temp != None:i_feedback+=temp 
        instructions = student.s_initialFeedback.splitlines() + [exefilename,
        f"Student : {student.s_name}",
        f"Grade   : {points[1]+points[0]}/{points[1]}", "Select an option:"]
        options = ["Edit File", "Recompile", "Regrade", "Continue"]
        while True:
            selectedData = self.o_uI.m_terminalUserInterface(options, instructions)
            if (selectedData == options[0]):
                self.m_editFile(filename)
            elif (selectedData == options[1]):
                output = self.m_compileCfile(proc)
                if (output):
                    self.o_uI.m_terminalUserInterface(["Continue"], "Compilation Successful")
                else:
                    self.o_uI.m_terminalUserInterface(["Continue"], output)
            elif (selectedData == options[2]):
                method = f"self.m_test{proc[-1]}(student,{proc[-1]},{points[1]})"
                exec(method)
            elif (selectedData == options[3]):
                student.f_grade+=points[0]
                student.s_initialFeedback += self.m_processFile(fileContent,i_feedback)
                student.s_initialFeedback +=f"\n-----------------------------------------------------------------------\n"
                break