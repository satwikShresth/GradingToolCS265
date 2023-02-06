from myLibs import os, parser, re, zipfile,PATH


class c_Student:
    def __init__(self, name, startPoints=100, submitLog="submit.log", gradeFile="grade.file", duedate="Thursday, February 2, 2023 11:59:59 PM EST"):
        self.name = name
        self.totalPoints = startPoints
        self.submitLog = submitLog
        self.feedbackFile = gradeFile
        self.feedback = self.m_InitFeedback()
        self.m_CheckSubmissionTime(duedate)

    def m_InitFeedback(self):
        return self.m_FeedbackHeader(os.path.join(os.getcwd(), self.name, self.submitLog)) + "Grade: ??\n\nFeedback:-\n"

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
            os.path.join(os.getcwd(), student, self.submitLog))
        timeSubmission = parser.parse(timeSubmission)
        timeDue = parser.parse(dueDate)
        timeDiffernce = timeDue - timeSubmission
        second = timeDiffernce.total_seconds()
        hours, remainder = divmod(abs(second), 3600)
        minutes, seconds = divmod(remainder, 60)

        if second < 0:

            if hours >= 1 and hours < 24:
                self.totalPoints -= 10
                self.feedback += f"{-10:<6} Late Submission:  {int(hours):02d}hours {int(minutes):02d}minutes {int(seconds):02d}seconds\n"
            elif hours >= 24 and hours < 48:
                self.totalPoints -= 20
                self.feedback += f"{-20:<6} Late Submission: {int(hours):02d}hours {int(minutes):02d}minutes {int(seconds):02d}seconds\n"
            elif hours >= 48:
                self.totalPoints = 0
                self.feedback += f"{0:<6} Late Submission:  {int(hours):02d}hours {int(minutes):02d}minutes {int(seconds):02d}seconds\n"

    def m_CheckSubmissionTime(self, duedate="Thursday, February 2, 2023 11:59:59 PM EST"):
        self._CheckSubmissionTime_(self.name, duedate)

    def m_CreateGradeFile(self):
        with open(os.path.join(os.getcwd(), self.name, self.feedbackFile), 'w') as file:
            file.write(self.feedback)

    def _Decompress_(self, student, filename):
        currentWorkingDir = os.getcwd()
        path = os.path.join(os.getcwd(), student)
        print(f'Changing working directory to {path}')
        os.chdir(path)

        with zipfile.ZipFile(filename, "r") as file:
            file.extractall()

        print(f'Changing working directory back to {currentWorkingDir}')
        os.chdir(currentWorkingDir)

    def m_Decompress(self, filename):
        if os.path.isfile(os.path.join(os.getcwd(), self.name, filename)):
            self._Decompress_(self.name, filename)
        else:
            ipt = "y"
            while (ipt != "q"):
                for file in os.listdir("."):
                    if os.path.isfile(file):
                        print(file)
                ipt = input("Give a file name[q to exit]: ")
                if ipt == "q":
                    self.feedback += f"{filename} does not exist\n"
                elif os.path.isfile(os.path.join(os.getcwd(), self.name, ipt)):
                    self._Decompress_(self.name, ipt)
                    self.feedback += f"Bad file name: {ipt} found instead of {filename}\n"
                    ipt = "q"
                else:
                    print("Try Again!!")
