from c_GradeMain import c_GradeMain
import os
import subprocess

from c_Student import c_Student
from c_TerminalUserInterface import c_termianlUserInterface

PATH = "/home/ss5278/GradeScript"


class c_AssignmentTrack():
    def __init__(self,uI: c_termianlUserInterface, assignment):
        self.o_uI= uI
        self.s_assignmentToGrade: str = assignment


    def m_initalizer(self):
        if self.s_assignmentToGrade == "Lab5":
            from c_GradeLab5 import c_GradeLab5
            return c_GradeLab5(self.o_uI)
        else:
            from c_GradeShell import c_GradeShell
            return c_GradeShell(self.o_uI,self.s_assignmentToGrade)

    def m_finalizeGrade(self, student: c_Student):
        student.s_feedback = student.s_feedback .replace(
            '?!?', str(student.f_grade) if student.f_grade >= 0 else str(0))

    def m_createFeedbackFile(self, filename: str, feedback: str):
        try:
            with open(filename, "w+") as f:
                f.write(feedback)
        except Exception as e:
            instructions = [f"Error:", f"{e}"]
            options = [f"Continue"]
            self.o_uI.m_terminalUserInterface(options, instructions)

    def m_compileTestingExe(self, output, input):
        if (self.m_compileCfile(["gcc", "-ldl", "-o", f"{PATH}/{output}", f"{PATH}/{input}"])):
            return output

    def m_Decompress(self,student:c_Student,filename):
        if os.path.isfile(filename):
            student.m_Decompress(filename)
            return True
        else:
            while (1):
                instructions = [
                    f"Student : {student.s_name}", f"Select a file for {filename}:"]
                options = [file for file in os.listdir(".")if os.path.isfile(file)] + ["No Need","No Files"]
                selectedData = self.o_uI.m_terminalUserInterface(options, instructions)
                if (options[-1] == selectedData):
                    return False
                elif (options[-2] == selectedData):
                    return True
                else:
                    student.s_initialFeedback += f"-----------------------------------------------------------------------\n"
                    student.s_initialFeedback += f"Bad file name: {selectedData} found instead of {filename}\n"
                    try:
                        student.m_Decompress(selectedData)
                        return True
                    except Exception as e:
                        instructions = [f"Error:", f"{e}"]
                        options = [f"Continue"]
                        data = self.o_uI.m_terminalUserInterface(options, instructions)
                        if data == options[0]:
                            continue


    def m_fileToStringList(self, filename):
        try:
            with open(filename, "r") as file:
                fileContents = [line for line in file.readlines() if line.strip()]
        except Exception as e:
            instructions = [f"Error:", f"{e}"]
            options = [f"Continue"]
            self.o_uI.m_terminalUserInterface(options, instructions)
        return fileContents

    def _CheckFile_(self, student: c_Student, filename, points):
        if os.path.isfile(filename):
            return filename
        else:
            instructions = [
                f"Student : {student.s_name}", f"Select a file for {filename}:"]
            options = [file for file in os.listdir(".")if os.path.isfile(file)]
            while (1):
                selectedData = self.o_uI.m_terminalUserInterface(
                     options, instructions)
                if (selectedData == "q"):
                    student.s_initialFeedback += f" {-points:<6} {filename} does not exist\n"
                    return False
                else:
                    instruction = self.m_fileToStringList(
                        selectedData)+[f"Is {selectedData} Correct?"]
                    option = ["Yes", "No"]
                    response = self.o_uI.m_terminalUserInterface(
                        option, instruction)
                    if (response == option[0]):
                        student.s_initialFeedback += f"Bad file name: {selectedData} found instead of {filename}\n"
                        student.s_initialFeedback += f"-----------------------------------------------------------------------\n"
                        return selectedData
            student.s_initialFeedback += f" {-points:<6} {filename} does not exist\n"
            return False

    def m_compileCfile(self, proc):
        result = subprocess.run(proc, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if result.returncode == 1:
            return result.stderr.decode()
        else:
            return True
    def m_showFile(self, filename: str):
        subprocess.run(["less", f"{filename}"])

    def m_editFile(self, filename: str):
        subprocess.run(["code", "-r", f"{filename}"])
