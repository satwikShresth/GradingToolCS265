import os
import re
from dateutil import parser
from zipfile import ZipFile

#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

class c_Student():
    def __init__(self, name:str,fullname:str, grader:str="Satwik Shresth", startPoints: float = 100, submitLog:str="submit.log", gradeFile:str="grade.file", duedate:str="Thursday, February 2, 2023 11:59:59 PM EST"):
        self.s_fullname: str = fullname
        self.s_name: str = name
        self.s_grader: str = grader
        self.f_grade: float = startPoints
        self.s_submitLog: str = submitLog
        self.s_feedbackFile: str = gradeFile
        self.s_initialFeedback: str = ""
        self.ls_filenames: list = []
        self.s_feedback: str = self.m_InitFeedback()
        self.dueDate= duedate
        self.m_CheckSubmissionTime()

    def m_Decompress(self,filename):
        if os.path.isfile(filename):
            with ZipFile(filename, "r") as file:
                file.extractall(".")
            os.remove(filename)
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    def m_InitFeedback(self) -> str:
        return self.m_FeedbackHeader(os.path.join(os.getcwd(), self.s_name, self.s_submitLog)) + f"Grader: {self.s_grader}\nGrade: ?!?\n\nFeedback:-\n"
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    def m_FeedbackHeader(self, filePath:str) -> str:
        with open(filePath, 'r') as file:
            lines = file.readlines()[:3]
        return "".join(lines)
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    def _ExtractDate_(self, filePath:str)->str:
        with open(filePath, 'r') as file:
            file_content = file.read()

        match = re.search(r'Date Submitted: (.*)', file_content)
        dateSubmitted = match.group(1)
        return dateSubmitted
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    def _CheckSubmissionTime_(self)->None:
        timeSubmission = self._ExtractDate_(
            os.path.join(os.getcwd(), self.s_name, self.s_submitLog))
        timeSubmission = parser.parse(timeSubmission)
        timeDue = parser.parse(self.dueDate)
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
    def m_CheckSubmissionTime(self):
        self._CheckSubmissionTime_()
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
