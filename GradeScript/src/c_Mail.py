from .c_GradeBook import c_GradeBook
from .c_Grader import c_Grader
import subprocess
import time


class c_Mail():
    def __init__(self, obj:str|object="",senderAddress="noreply@cs265.drexel.edu", s_subject="Feedback for Lab5", s_grader="Satwik Shresth"):
        if type (obj) == c_GradeBook:
            self.o_gradeMain: c_GradeBook = obj
        else:
            self.obj = obj
        self.s_senderAddress: str = senderAddress
        self.s_subject: str = s_subject
        self.footer = f"\nBest,\n{s_grader}\nBSc Computer Science\nCollege of Computing and Informatics\nDrexel University\nPhiladelphia, PA 19104\nsatwik.shresth@drexel.edu\n"

    def m_addFooter(self, student, file):
        try:
            with open(f"{student}/{file}", 'a') as file:
                file.write(self.footer)
        except Exception as e:
            print(f"Error:", f"{e}")
            
    def m_sendMail(self, students, filename="grade.file"):
        for student in students:
            if student in self.o_gradeMain.d_listOfStudentsGraded.keys():
                self.m_addFooter(student, filename)
                mailCmd = f"cat {student}/{filename} | mail -s '{self.s_subject}' -r '{self.s_senderAddress}' {student}@drexel.edu"
                result = subprocess.run(
                    mailCmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                if result.returncode == 0:
                    print(f'Feedback sent to {student} successfully.')
                    time.sleep(.5)
                else:
                    print('An error occurred while sending the email:',
                          result.stderr.decode().strip())
        input("press anything to continue...")


    def m_sendInstructions(self,instructions,belowInstructions,toPerson):
        mail = instructions+belowInstructions+"\n\n\n"+self.footer
        mailCmd = f"echo '{mail}' | mail -s '{self.s_subject}' -r '{self.s_senderAddress}' {toPerson}@drexel.edu"
        result = subprocess.run(mailCmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if result.returncode == 0:
            print(f'Instructions sent to {toPerson} successfully.')
            time.sleep(.5)
        else:
            print('An error occurred while sending the email:',
                    result.stderr.decode().strip())
        input("press anything to continue...")





