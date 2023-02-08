from c_GradeMain import c_GradeMain
import subprocess
import time


class c_Mail():
    def __init__(self, GradeMain: c_GradeMain, senderAddress="noreply@cs265.drexel.edu", s_subject="Feedback for Lab5"):
        self.o_gradeMain:c_GradeMain = GradeMain
        self.s_senderAddress:str = senderAddress
        self.s_subject:str = s_subject

    def m_sendMail(self, students, file="grade.file"):
        for student in students:
            if student in self.o_gradeMain.ss_listOfStudentsGraded:

                mailCmd = f"cat {student}/{file} | mail -s '{self.s_subject}' -r '{self.s_senderAddress}' {student}@drexel.edu"
                result = subprocess.run(
                    mailCmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                if result.returncode == 0:
                    print(f'Feedback sent to {student} successfully.')
                    time.sleep(.5)
                else:
                    print('An error occurred while sending the email:',
                          result.stderr.decode().strip())
