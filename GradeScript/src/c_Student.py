import os
import subprocess
from dateutil import parser
from zipfile import ZipFile
TOOLS = "/home/ss5278/GradeScript/tools"
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

class c_Student():
    def __init__(self, name:str, startPoints: float = 100, submitLog:str="submit.log", gradeFile:str="grade.file"):
        self.s_fullname: str
        self.s_name: str = name
        self.submissions = {}
        self.f_grade: float = startPoints
        self.s_submitLog: str = submitLog
        self.s_feedbackFile: str = gradeFile
        self.m_initalizeCurrentGrader()
        self.m_initlaizeStudent()
        self.s_initialFeedback: str = ""
        self.ls_filenames:dict = {}
        self.s_feedback: str = self.m_InitFeedback()
        self.parsedAnswers:dict


    
    def m_loadProfile(self,assignment):
        submission = None

        try:
            lines = self.m_FeedbackHeader(os.path.join(os.getcwd(), self.s_name, self.s_submitLog))
            for line in lines:
                if "Assignment:" in line:
                    self.assignment = str(line.split("Assignment: ")[1].strip())
                if "Date Submitted:" in line:
                    submission = str(line.split("Date Submitted: ")[1].strip())
        except:
            self.assignment = assignment
        
        self.submissions[self.assignment] = submission
        self.m_initalizeCurrentGrader()
        self.s_feedback = self.m_InitFeedback()
        self.s_initialFeedback: str = ""


#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    def m_initalizeCurrentGrader(self):
        self.s_grader = os.getcwd().split("/")[2]
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    def m_initlaizeStudent(self):
        lines = self.m_FeedbackHeader(os.path.join(os.getcwd(), self.s_name, self.s_submitLog))
        for line in lines:
            if "Name:" in line:
                self.s_fullname = str(line.split("Name: ")[1].strip())
            if "Assignment:" in line:
                self.assignment = str(line.split("Assignment: ")[1].strip())
            if "Date Submitted:" in line:
                submission = str(line.split("Date Submitted: ")[1].strip())

        self.submissions[self.assignment] = submission
        

        

#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    def m_Decompress(self,filename):
        if os.path.isfile(filename):
            with ZipFile(filename, "r") as file:
                file.extractall(".")
            os.remove(filename)
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    def m_InitFeedback(self) -> str:
        return f"Name: {self.s_fullname}\nAssignment: {self.assignment}\nDate Submitted: {self.submissions[self.assignment]}\nGrader: {self.s_grader}\nGrade: ?!?\n\nFeedback:-\n"
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    def m_FeedbackHeader(self, filePath) -> str:
        with open(filePath, 'r') as file:
            lines = file.readlines()[:3]
        return lines
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    def m_editFile(self,filename=None):
        micro = os.path.join(TOOLS,"micro")
        if filename is not None:
            subprocess.run([micro, f"{filename}"])
        else:
            subprocess.run([micro, f"{self.s_feedbackFile}"])
        

#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    def m_showFile(self,filename=None):
        if filename is not None:
            subprocess.run(["less", f"{filename}"])
        else:
            subprocess.run(["less", f"{self.s_feedbackFile}"])

#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    def m_fileToStringList(self, filename):
        with open(filename, "r") as file:
            fileContents = [line for line in file.readlines() if line.strip()]
        return fileContents
    
    def m_registerGrade(self):
        content = self.m_fileToStringList(self.s_feedbackFile)
        for line in content:
            if "Grade:" in line:
                grade = float(line.split("Grade:")[1].strip())
                self.f_grade = grade
            if "Name:" in line:
                self.s_fullname = str(line.split("Name: ")[1].strip())
        

#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    def m_CheckSubmissionTime(self,dueDate,assignmentName):
        timeSubmission = self.submissions[assignmentName]
        if timeSubmission != None:
            timeSubmission = parser.parse(timeSubmission)
            timeDue = parser.parse(dueDate)
            timeDiffernce = timeDue - timeSubmission
            second = timeDiffernce.total_seconds()
            hours, remainder = divmod(abs(second), 3600)
            minutes, seconds = divmod(remainder, 60)

            if second < 0:

                if hours >= 1 and hours < 24:
                    self.f_grade -= 10
                    self.s_feedback += f" {-10:<6} Late Submission:  {int(hours):02d}hours {int(minutes):02d}minutes {int(seconds):02d}seconds\n"
                elif hours >= 24 and hours < 48:
                    self.f_grade -= 20
                    self.s_feedback += f" {-20:<6} Late Submission: {int(hours):02d}hours {int(minutes):02d}minutes {int(seconds):02d}seconds\n"
                elif hours >= 48:
                    self.f_grade = 0
                    self.s_feedback += f" {0:<6} Late Submission:  {int(hours):02d}hours {int(minutes):02d}minutes {int(seconds):02d}seconds\n"
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
