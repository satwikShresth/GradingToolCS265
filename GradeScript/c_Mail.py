from c_GradeMain import c_GradeMain
import subprocess,time

class c_Mail():
    def __init__(self,GradeMain:c_GradeMain,senderAddress="noreply@cs265.drexel.edu",subject="Feedback for Lab5"):
        self.gradeMain=GradeMain
        self.senderAddress=senderAddress
        self.subject=subject
        self.funFact = "\n\nFun Fact: Your assignment is graded and mailed using tools created by all the cool language and programming techniques taught in this class\n"
        self.footer = '''\nBest,
        Satwik Shresth
        BSc Computer Science
        College of Computing and Informatics
        Drexel University
        Philadelphia, PA 19104
        satwik.shresth@drexel.edu
        '''


    def m_sendMail(self,students,file="grade.file"):
        for student in students:
            if student in self.gradeMain.listOfStudentsGraded:

                mailCmd = f"cat {student}/{file} | mail -s '{self.subject}' -r '{self.senderAddress}' {student}@drexel.edu"
                result = subprocess.run(mailCmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                if result.returncode == 0:
                    print(f'Feedback sent to {student} successfully.')
                    time.sleep(.5)
                else:
                    print('An error occurred while sending the email:', result.stderr.decode().strip())
