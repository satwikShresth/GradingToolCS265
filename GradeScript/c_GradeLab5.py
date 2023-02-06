from myLibs import os, parser, re, zipfile,PATH,c_GradeMain,subprocess,json,difflib



class c_GradeLab5():
    def __init__(self,GradeMain,filesReq="lab5_1.c lab5_2.c lab5_3.c",zipFile="lab5.zip"):
        self.GradeMain = GradeMain
        self.filesReq = filesReq.split()
        if (zipFile != None):
            self.zipFile=zipFile
        self.gradeQuickSortExe = self.compileTestingExe("testQuickSort","testQuickSort.c")
        self.gradeSplitExe = self.compileTestingExe("testSplit","testSplit.c")
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


    def compileTestingExe(self,output,input):
        if(self.m_compileCfile(["gcc", "-ldl", "-o",f"{PATH}/{output}",f"{PATH}/{input}"])):
            return output

    def m_Decompress(self):
        for student in self.GradeMain.listOfStudents.values():
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
                    student.feedback+= f"{-10:<6} {filename} does not exist\n"
                    return False
                elif os.path.isfile(ipt):
                    student.feedback+= f"Bad file name: {ipt} found instead of {filename}\n"
                    return ipt
                else:
                    print("Try Again!!")

    def m_compileCfile(self,proc):
        result = subprocess.run(proc, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if result.returncode != 0:
            print(result.stderr.decode(), end="")
            return False
        else:
            return True

    def m_testExecutableQuestion1(self,student,outputFile):
        pointsDeduct=0
        for testString in self.testStringsQ1:
            process = subprocess.Popen([f"./{outputFile}"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
            output, error = process.communicate(input=testString.encode('utf-8'))
            output = output.decode(errors='ignore')
            output =":".join(output.split(":")[2::])
            matcher = difflib.SequenceMatcher(None, output, testString[::-1])
            similarity = matcher.ratio() * 100
            if (similarity>96):
                student.totalPoints+=.5
            else:
                pointsDeduct=-.5
                student.feedback+= f"{-.5:<6}Failed Test String      -> {testString}\n"
                student.feedback+= f"{'':6}your ouput              -> {output}\n"
                student.feedback+= f"{'':6}desired output          -> {testString[::-1]}\n"
                student.feedback+= f"{'':6}Similarity Percent      -> {similarity}\n"
        return pointsDeduct
    def m_testExecutableQuestion3(self,student,testExe,outputFile):
        process = subprocess.Popen([f"{PATH}/{testExe} ./{outputFile}"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE,shell=True,universal_newlines=True)
        output, _ = process.communicate()
        output =list(filter(None,output.split('\n')))
        if "Caught Segmentation Fault" in output:
            student.feedback+= f"{-5:<6}Function implementation is wrong\n"
            return
        dict = {}
        points = 5
        if len(output) >= 1:
            for dictIter in output:
                dict.update((json.loads(json.loads(json.dumps(dictIter)))))
                points =- 1
            for key, value in dict.items():
                student.feedback+= f"{-.5:<6}Failed Test String      -> {self.testStringsQ3[key][0]}\n"
                student.feedback+= f"{'':6}your ouput              -> {value}\n"
                student.feedback+= f"{'':6}desired output          -> {self.testStringsQ3[key][1]}\n"

        else:
            student.feedback+= f"{'':6}All Test Strings Passed\n"

    def m_CheckQuestion1(self,student):
        student = self.GradeMain.listOfStudents[student]
        student.feedback+= f"\nPart-1 Reverse the string\n"
        currentWorkingDir = os.getcwd()
        path =os.path.join(os.getcwd(), student.name)
        # print(f'Changing working directory to {path}')
        os.chdir(path)
        filename = self._CheckFile_(student,self.filesReq[0])
        if( filename != False):
            
            output = "Question1"
            if(self.m_compileCfile(["gcc", filename, "-o", output])):
                pointDeducted = self.m_testExecutableQuestion1(student,output)
                if( pointDeducted ==0):
                    student.feedback+= f"{'':6} All test strings passed\n"
                else:
                    student.totalPoints-=pointDeducted
            else:
                student.feedback+= f"{-5:<6} Compilation Error\n"
                student.totalPoints-=5
        # print(f'Changing working directory back to {currentWorkingDir}')
        os.chdir(currentWorkingDir)

    def m_CheckQuestion2(self,student):
        student = self.GradeMain.listOfStudents[student]
        student.feedback+= f"\nPart-2 Reverse the string[*pointers]\n"
        currentWorkingDir = os.getcwd()
        path =os.path.join(os.getcwd(), student.name)
        # print(f'Changing working directory to {path}')
        os.chdir(path)
        filename = self._CheckFile_(student,self.filesReq[1])
        if( filename != False):

            output = "Question2"
            if(self.m_compileCfile(["gcc", filename, "-o", output])):
                subprocess.run(["less", f"{filename}"])
                while(1):
                    grade = int(input("Grade[?/5]: "))
                    if grade > 0 and grade <6:
                        feedback = input("Feedback: ")
                        student.totalPoints+=(grade-5)
                        if (grade-5) == 0:
                            student.feedback+= f"{' ':6} {feedback}\n"
                        else:
                            student.feedback+= f"{(grade-5):<6} {feedback}\n"
                        pointDeducted = self.m_testExecutableQuestion1(student,output)
                        if( pointDeducted ==0):
                            student.feedback+= f"{'':6} All test strings passed\n"
                        else:
                            student.totalPoints-=pointDeducted
                        break
                    elif grade==0:
                        student.feedback+= f"{-10:<6} Did not follow the instructions!\n"
                        break

            else:
                student.feedback+= f"{-5:<6} Compilation Error\n"
                student.totalPoints-=5
        # print(f'Changing working directory back to {currentWorkingDir}')
        os.chdir(currentWorkingDir)

    def m_CheckQuestion3(self,student):
        student = self.GradeMain.listOfStudents[student]
        student.feedback+= f"\nPart-3 Modifying split function accept 1 array, 2 int* and return int*\n"
        currentWorkingDir = os.getcwd()
        path =os.path.join(os.getcwd(), student.name)
        # print(f'Changing working directory to {path}')
        os.chdir(path)
        filename = self._CheckFile_(student,self.filesReq[2])
        if( filename != False):
            output = "Question3.so"
            if(self.m_compileCfile(["gcc","-shared","-o",output,filename])):
                student.feedback+= f"{'':2}Testing QuickSort Function\n"
                self.m_testExecutableQuestion3(student,self.gradeQuickSortExe,output)
                student.feedback+= f"{'':2}Testing Split Function\n"
                self.m_testExecutableQuestion3(student,self.gradeSplitExe,output)
            else:
                student.feedback+= f"{-5:<6} Compilation Error\n"
                student.totalPoints-=5
        # print(f'Changing working directory back to {currentWorkingDir}')
        os.chdir(currentWorkingDir)
