import os,sys
import subprocess
from .c_Student import c_Student
from .c_TerminalUserInterface import c_termianlUserInterface

PATH = "/home/ss5278/GradeScript"


class c_AssignmentTrack():
    def __init__(self,uI: c_termianlUserInterface, assignment,data):
        self.o_uI= uI
        self.s_assignmentToGrade: str = assignment
        self.data = data
#--------------------------------------------------------------------------------------------------------------------------------------
    def m_initalizer(self):
        from .c_GradeCommon import c_GradeCommon
        return c_GradeCommon(self.o_uI,self.data)            

#--------------------------------------------------------------------------------------------------------------------------------------
    def m_finalizeGrade(self, student: c_Student):
        student.s_feedback = student.s_feedback .replace(
            '?!?', str(student.f_grade) if student.f_grade >= 0 else str(0))

#--------------------------------------------------------------------------------------------------------------------------------------
    def m_createFeedbackFile(self, filename: str, feedback: str):
        try:
            with open(filename, "w+") as f:
                f.write(feedback)
        except Exception as e:
            instructions = [f"Error:", f"{e}"]
            options = [f"Continue"]
            self.o_uI.m_terminalUserInterface(options, instructions)

#--------------------------------------------------------------------------------------------------------------------------------------
    def m_compileTestingExe(self, output, input):
        if (self.m_compileCfile(["gcc", "-ldl", "-o", f"{PATH}/{output}", f"{PATH}/{input}"])):
            return output

#--------------------------------------------------------------------------------------------------------------------------------------
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


#--------------------------------------------------------------------------------------------------------------------------------------
    def m_filesToStringList(self, filename):
        fileContents = []
        if type(filename)==str:
            filename = [filename]
        for file in filename:
            try:
                with open(file, "r") as f:
                    fileContents += [f"|--------------------------| {file} |--------------------------|"]
                    fileContents += [line for line in f.readlines() if line.strip()]
                return fileContents
            except Exception as e:
                instructions = [f"Error:", f"{e}"]
                options = [f"Continue"]
                self.o_uI.m_terminalUserInterface(options, instructions)
                sys.exit(1)
        

#--------------------------------------------------------------------------------------------------------------------------------------
    def _CheckFile_(self, student: c_Student, filename):
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
                    student.s_initialFeedback += f"{filename} does not exist\n"
                    return False
                else:
                    instruction = self.m_filesToStringList(
                        selectedData)+[f"Is {selectedData} Correct?"]
                    option = ["Yes", "No"]
                    response = self.o_uI.m_terminalUserInterface(
                        option, instruction)
                    if (response == option[0]):
                        student.s_initialFeedback += f"Bad file name: {selectedData} found instead of {filename}\n"
                        student.s_initialFeedback += f"-----------------------------------------------------------------------\n"
                        return selectedData
            student.s_initialFeedback += f"{filename} does not exist\n"
            return False

#--------------------------------------------------------------------------------------------------------------------------------------
    def m_compileCfile(self, proc):
        result = subprocess.run(proc, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if result.returncode == 1:
            return result.stderr.decode()
        else:
            return True

#--------------------------------------------------------------------------------------------------------------------------------------
    def m_gradedReport(self, student: c_Student):
        student.m_showFile()
        instructions = [f"Student : {student.s_name}",
                        f"Grade   : {student.f_grade}/100", "Select an option:"]
        options = ["Edit grade.file", "Show grade.file", "Continue"]
        while True:
            selectedData = self.o_uI.m_terminalUserInterface(
                options, instructions)
            if (selectedData == options[0]):
                self.o_uI.m_end()
                student.m_editFile()
                self.o_uI.m_restart()
            elif (selectedData == options[1]):
                self.o_uI.m_end()
                student.m_showFile()
                self.o_uI.m_restart()
            elif (selectedData == options[2]):
                break
#--------------------------------------------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------------------------------------------
    def m_processFile(self,fileContentList:list,i_feedback):
        file = f"\n".join([i for i in fileContentList if i != ""])
        i_feedback = "\n"+ f"\n{'':4}* ".join(i_feedback)
        return file + i_feedback
    

#--------------------------------------------------------------------------------------------------------------------------------------
    def m_selectFileAction(self,student:c_Student,action,files):
        while (1):
            instructions = [f"Select a file:"]
            options = [file for file in os.listdir(".") if os.path.isfile(file) and file in files]
            selectedData = self.o_uI.m_terminalUserInterface(options, instructions)
            if (selectedData == "q"):
                break
            else:
                instruction = self.m_filesToStringList(selectedData)+[f"Is {selectedData} Correct?"]
                option = ["Yes", "No"]
                response = self.o_uI.m_terminalUserInterface(
                    option, instruction)
                if (response == option[0]):
                    if action == "edit":
                        self.o_uI.m_end()
                        student.m_editFile(selectedData)
                        self.o_uI.m_restart()
                    elif action == "show":
                        self.o_uI.m_end()
                        student.m_showFile(selectedData)
                        self.o_uI.m_restart()
                    break