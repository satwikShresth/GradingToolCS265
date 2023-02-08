from c_GradeMain import c_GradeMain
import os
import subprocess
import curses
from c_Student import c_Student
from c_TerminalUserInterface import c_termianlUserInterface

PATH = "/home/ss5278/GradeScript"


class c_AssignmentTrack():
    def __init__(self, GradeMain: c_GradeMain, assignment):
        self.uI:c_termianlUserInterface = c_termianlUserInterface()
        self.gradeMain:c_GradeMain = GradeMain
        self.assignmentToGrade:str = assignment
        self.zipFile:str = ""
        self.funFact:str = f"\n\nFun Fact: Your assignment is graded and mailed to you using a script.\n{' ':10}It created by all the cool proggramming language, techniques and tools you are learning in this class\n{' ':10}i.e. Bash,C,awk,grep,python,cat"
        self.foote:str = "\nBest,\nSatwik Shresth\nBSc Computer Science\nCollege of Computing and Informatics\nDrexel University\nPhiladelphia, PA 19104\nsatwik.shresth@drexel.edu\n"

    def m_initalizer(self):
        if self.assignmentToGrade == "Lab5":
            from c_GradeLab5 import c_GradeLab5
            return c_GradeLab5(self.gradeMain)
        else:
            from c_GradeShell import c_GradeShell
            return c_GradeShell(self.gradeMain,self.assignmentToGrade)

    def m_finalizeGrade(self, student: c_Student):
        student.s_initialFeedback = student.s_initialFeedback .replace(
            '?!?', str(student.f_grade))

    def m_createFeedbackFile(self, filename: str, feedback: str):
        with open(filename, "w+") as f:
            f.write(feedback)

    def m_compileTestingExe(self, output, input):
        if (self.m_compileCfile(["gcc", "-ldl", "-o", f"{PATH}/{output}", f"{PATH}/{input}"])):
            return output

    def m_Decompress(self):
        for student in self.gradeMain.d_listOfStudents.values():
            student.m_Decompress(self.zipFile)

    def _CheckFile_(self, student, filename):
        if os.path.isfile(filename):
            return filename
        else:
            instructions = [
                f"Student : {student.name}", f"Select a file for {filename}:"]
            options = [file for file in os.listdir(".")if os.path.isfile(file)]
            while (1):
                screen = curses.initscr()
                selectedData = self.uI.m_terminalUserInterface(
                    screen, options, instructions)
                curses.endwin()
                if (selectedData == "q"):
                    student.initialFeedback += f" {-10:<6} {filename} does not exist\n"
                    return False
                else:
                    self.m_showFile(selectedData)
                    instructions = [f"Is {selectedData} Correct?"]
                    options = ["Yes", "No"]
                    screen = curses.initscr()
                    ans = self.uI.m_terminalUserInterface(
                        screen, options, instructions)
                    curses.endwin()
                    if (ans != "n"):
                        student.initialFeedback += f"Bad file name: {selectedData} found instead of {filename}\n"
                        return selectedData

    def m_compileCfile(self, proc):
        result = subprocess.run(
            proc, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if result.returncode != 0:
            return result.stderr.decode()
        else:
            return True

    def m_showFile(self, filename: str):
        subprocess.run(["less", f"{filename}"])

    def m_editFile(self, filename: str):
        subprocess.run(["code", "-r", f"{filename}"])
