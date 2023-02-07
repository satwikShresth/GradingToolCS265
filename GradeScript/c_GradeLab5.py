import os,subprocess,json,difflib
from c_GradeMain import c_GradeMain
from c_Student import c_Student

PATH="/home/ss5278/GradeScript"

class c_GradeLab5():
    def __init__(self,GradeMain:c_GradeMain,filesReq="lab5_1.c lab5_2.c lab5_3.c",zipFile="lab5.zip"):
        self.gradeMain = GradeMain
        self.filesReq = filesReq.split()
        if (zipFile != None):
            self.zipFile=zipFile
        self.gradeQuickSortExe = self.m_compileTestingExe("testQuickSort","testQuickSort.c")
        self.gradeSplitExe = self.m_compileTestingExe("testSplit","testSplit.c")
        self.testStringsQ1 = [
            "Go home, relax. Reverse this string.",
            "Can you handle this? Reverse it.",
            "A quick brown fox jumps over the lazy dog. Reverse.",
            "Easy come, easy go. Reverse it now.",
            "Action speaks louder than words. Reverse this.",
            "Too good to be true. Reverse this statement.",
            "All good things come to those who wait. Reverse it.",
            "Practice makes perfect. Reverse this phrase.",
            "Nothing is impossible. Reverse this belief.",
            "Where there's a will, there's a way. Reverse it."
            ]
        self.testStringsQ3 = {
            "1":[[734, 896, 402, 977, 781, 671, 212, 163, 679, 502],[163, 212, 402, 502, 671, 679, 734, 781, 896, 977]],
            "2":[[194, 732, 243, 952, 719, 812, 603, 541, 890, 910],[194, 243, 541, 603, 719, 732, 812, 890, 910, 952]],
            "3":[[367, 991, 784, 546, 310, 165, 886, 969, 807, 527],[165, 310, 367, 527, 546, 784, 807, 886, 969, 991]],
            "4":[[956, 879, 566, 793, 642, 623, 233, 474, 168, 713],[168, 233, 474, 566, 623, 642, 713, 793, 879, 956]],
            "5":[[758, 191, 903, 443, 526, 986, 849, 598, 126, 660],[126, 191, 443, 526, 598, 660, 758, 849, 903, 986]]
        }
        self.funFact = f"\n\nFun Fact: Your assignment is graded and mailed to you using a script.\n{' ':10}It created by all the cool proggramming language, techniques and tools you are learning in this class\n{' ':10}i.e. Bash,C,awk,grep,python,cat"
        self.footer = "\nBest,\nSatwik Shresth\nBSc Computer Science\nCollege of Computing and Informatics\nDrexel University\nPhiladelphia, PA 19104\nsatwik.shresth@drexel.edu\n"


    def m_finalizeGrade(self,student:c_Student):
        student.feedback = student.feedback.replace('?!?',str(student.grade))
    def m_gradeLab5(self,name):
        student = self.gradeMain.listOfStudents[name]
        currentWorkingDir = os.getcwd()
        path =os.path.join(os.getcwd(),name)
        # print(f'Changing working directory to {path}')
        os.chdir(path)
        self.m_CheckQuestion1(student)
        self.m_CheckQuestion2(student)
        self.m_CheckQuestion3(student)
        self.m_finalizeGrade(student)
        student.feedback+= self.funFact
        student.feedback+= self.footer
        self.m_createFeedbackFile(student)
        self.m_gradedReport(student)
        # print(f'Changing working directory back to {currentWorkingDir}')
        os.chdir(currentWorkingDir)


    def m_createFeedbackFile(self,student:c_Student):
        with open(student.feedbackFile, "w+") as f:
            f.write(student.feedback)


    def m_compileTestingExe(self,output,input):
        if(self.m_compileCfile(["gcc", "-ldl", "-o",f"{PATH}/{output}",f"{PATH}/{input}"])):
            return output

    def m_Decompress(self):
        for student in self.gradeMain.listOfStudents.values():
            student.m_Decompress(self.zipFile) 

    def _CheckFile_(self,student,filename):
        if os.path.isfile(filename):
            return filename
        else:
            print("Files available:-")
            for file in os.listdir("."):
                if os.path.isfile(file):
                    print(file, end=" ")
            while(1):
                ipt=input("\nGive a file name[q to exit/doesn't exist]: ")
                if ipt == "q":
                    student.feedback+= f" {-10:<6} {filename} does not exist\n"
                    return False
                elif os.path.isfile(ipt):
                    student.feedback+= f"Bad file name: {ipt} found instead of {filename}\n"
                    return ipt
                else:
                    print("Try Again!!")

    def m_compileCfile(self,proc):
        result = subprocess.run(proc, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if result.returncode != 0:
            return result.stderr.decode()
        else:
            return True

    def m_testExecutableQuestion1(self,student:c_Student,outputFile):
        pointsDeduct=0
        for testString in self.testStringsQ1:
            process = subprocess.Popen([f"./{outputFile}"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
            output, error = process.communicate(input=testString.encode('utf-8'))
            output = output.decode(errors='ignore')
            output =":".join(output.split(":")[2::])
            matcher = difflib.SequenceMatcher(None, output, testString[::-1])
            similarity = matcher.ratio() * 100
            if (similarity<96):
                pointsDeduct+=.5
                student.feedback+= f" {-.5:<6}Failed Test String      -> {testString}\n"
                student.feedback+= f" {'':6}your ouput              -> {output}\n"
                student.feedback+= f" {'':6}desired output          -> {testString[::-1]}\n"
                student.feedback+= f" {'':6}Similarity Percent      -> {similarity}\n"
                student.feedback+= f"-----------------------------------------------------------------------\n"
        return pointsDeduct

    def m_testExecutableQuestion3(self,student:c_Student,testExe,outputFile):
        process = subprocess.Popen([f"{PATH}/{testExe} ./{outputFile}"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE,shell=True,universal_newlines=True)
        output, _ = process.communicate()
        output =list(filter(None,output.split('\n')))
        if "Caught Segmentation Fault" in output:
            student.feedback+= f" {-5:<6}Function implementation is wrong\n"
            student.feedback+= f"-----------------------------------------------------------------------\n"
            return
        dict = {}
        points = 0
        if len(output) >= 1:
            for dictIter in output:
                dict.update((json.loads(json.loads(json.dumps(dictIter)))))
                student.grade -= 1
            for key, value in dict.items():
                student.feedback+= f" {-1:<6}Failed Test String      -> {self.testStringsQ3[key][0]}\n"
                student.feedback+= f" {'':6}your ouput              -> {value}\n"
                student.feedback+= f" {'':6}desired output          -> {self.testStringsQ3[key][1]}\n"
                student.feedback+= f"-----------------------------------------------------------------------\n"

        else:
            student.feedback+= f"{'':6}All Test Strings Passed\n"
            student.feedback+= f"-----------------------------------------------------------------------\n"

    def m_feedbackLoop(self,student:c_Student,filename,outOf):
        subprocess.run(["less", f"{filename}"])
        while(1):
            grade = input(f"Grade[?/{outOf}]: ")
            if grade.isdigit():
                grade = int(grade)
                if grade > 0 and grade <outOf+1:
                    feedback = input("Feedback: ")
                    student.grade+=(grade-outOf)
                    if (grade-outOf) == 0:
                        student.feedback+= f"{' ':6} {feedback}\n"
                    else:
                        student.feedback+= f" {(grade-outOf):<6} {feedback}\n"
                    break


    def m_compilationError(self,student:c_Student,filename,error,outOf):
        student.feedback+= f" {-5:<6} Compilation Error: {error}"
        student.grade-=5
        self.m_feedbackLoop(student,filename,outOf)

    def m_CheckQuestion1(self,student:c_Student):
        student.feedback+= f"\nPart-1 Reverse the string\n"
        student.feedback+= f"-----------------------------------------------------------------------\n"
        filename = self._CheckFile_(student,self.filesReq[0])
        if( filename != False):
            output = "Question1"
            notError = self.m_compileCfile(["gcc", filename, "-o", output])
            if(notError == True):
                pointDeducted = self.m_testExecutableQuestion1(student,output)
                if( pointDeducted ==0):
                    student.feedback+= f"{'':6} All test strings passed\n"
                self.m_feedbackLoop(student,filename,5)
                student.grade-=pointDeducted
            else:
                self.m_compilationError(student,filename,notError,5)
                

    def m_CheckQuestion2(self,student:c_Student):
        student.feedback+= f"\nPart-2 Reverse the string[*pointers]\n"
        student.feedback+= f"-----------------------------------------------------------------------\n"
        filename = self._CheckFile_(student,self.filesReq[1])
        if( filename != False):
            output = "Question2"
            notError = self.m_compileCfile(["gcc", filename, "-o", output])
            if(notError == True):
                subprocess.run(["less", f"{filename}"])
                while(1):
                    grade = input("Grade[?/5]: ")
                    if grade.isdigit():
                        grade = int(grade)
                        if grade > 0 and grade <6:
                            feedback = input("Feedback: ")
                            student.grade+=(grade-5)
                            if (grade-5) == 0:
                                student.feedback+= f"{' ':6} {feedback}\n"
                            else:
                                student.feedback+= f" {(grade-5):<6} {feedback}\n"
                            pointDeducted = self.m_testExecutableQuestion1(student,output)
                            if( pointDeducted ==0):
                                student.feedback+= f" {'':6}All test strings passed\n"
                            else:
                                student.grade-=pointDeducted
                            break

                        elif grade==0:
                            student.feedback+= f" {-10:<6} Did not follow the instructions!\n"
                            student.grade-=10
                            break
            else:
                self.m_compilationError(student,filename,notError,5)

    def m_CheckQuestion3(self,student:c_Student):
        student.feedback+= f"\nPart-3 Modifying split function accept 1 array, 2 int* and return int*\n"
        student.feedback+= f"-----------------------------------------------------------------------\n"
        filename = self._CheckFile_(student,self.filesReq[2])
        if( filename != False):
            output = "Question3.so"
            notError = self.m_compileCfile(["gcc","-shared","-o",output,filename])
            if(notError == True):
                student.feedback+= f"Testing QuickSort Function\n"
                self.m_testExecutableQuestion3(student,self.gradeQuickSortExe,output)
                student.feedback+= f"Testing Split Function\n"
                self.m_testExecutableQuestion3(student,self.gradeSplitExe,output)
                self.m_feedbackLoop(student,filename,10)
            else:
                self.m_compilationError(student,filename,notError,10)

    def m_showGradeFile(self,student:c_Student):
        subprocess.run(["less", f"{student.feedbackFile}"])
    
    def m_editGradeFile(self,student:c_Student):
        subprocess.run(["code","-r", f"{student.feedbackFile}"])

        
    def m_gradedReport(self,student:c_Student):
        print(f"------------------------------------------------------------------------------")
        print(f"Student : {student.name}")
        print(f"Grade   : {student.grade}")
        print(f"---------------------------")
        print(f"Options:")
        print(f"---------------------------")
        print(f"(E)dit    - Edit grade.file")
        print(f"(S)how    - Show grade.file")
        print(f"(C)    - To continue")
        print(f"---------------------------")
        while True:
                userInput = input(f"Enter Action: ")
                match userInput.lower():
                    case "e":
                        self.m_editGradeFile(student)
                    case "s":
                        self.m_showGradeFile(student)
                    case "c":
                        break
                    case _:
                        print("try again")
                        continue