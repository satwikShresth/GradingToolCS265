import os
import re
from dateutil import parser


class c_Student():
    def __init__(self, name, grader="Satwik Shresth", startPoints: float = 100, submitLog="submit.log", gradeFile="grade.file", duedate="Thursday, February 2, 2023 11:59:59 PM EST"):
        self.s_name:str = name
        self.s_grader:str = grader
        self.f_grade:float = startPoints
        self.s_submitLog:str = submitLog
        self.s_feedbackFile:str = gradeFile
        self.s_initialFeedback:str = self.m_InitFeedback()
        self.ls_filenames:list = []
        self.s_feedback:str = self.m_InitFeedback()
        self.m_CheckSubmissionTime(duedate)

    def m_InitFeedback(self):
        return self.m_FeedbackHeader(os.path.join(os.getcwd(), self.s_name, self.s_submitLog)) + f"Grader: {self.s_grader}\nGrade: ?!?\n\nFeedback:-\n"

    def m_FeedbackHeader(self, filePath) -> str:
        with open(filePath, 'r') as file:
            lines = file.readlines()[:3]
        return "".join(lines)

    def _ExtractDate_(self, filePath):
        with open(filePath, 'r') as file:
            file_content = file.read()

        match = re.search(r'Date Submitted: (.*)', file_content)
        dateSubmitted = match.group(1)
        return dateSubmitted

    def _CheckSubmissionTime_(self, student, dueDate):
        timeSubmission = self._ExtractDate_(
            os.path.join(os.getcwd(), student, self.s_submitLog))
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

    def m_CheckSubmissionTime(self, duedate="Thursday, February 2, 2023 11:59:59 PM EST"):
        self._CheckSubmissionTime_(self.s_name, duedate)

    def m_CreateGradeFile(self):
        with open(os.path.join(os.getcwd(), self.s_name, self.s_feedbackFile), 'w') as file:
            file.write(self.s_feedback)