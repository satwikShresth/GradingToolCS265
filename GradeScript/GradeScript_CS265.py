import os
import sys
import re,datetime
from dateutil import parser
import zipfile
import subprocess
import difflib
import json



PATH="/home/ss5278/GradeScript"

class c_DirOrganizer:
    def __init__(self):
        pass

    def m_SplitAndStore(self,inputString, delimiter):
        splitList = inputString.split(delimiter)
        fileName = splitList[4] if len(splitList) >= 5 else "submit.log"
        directoryName = splitList[1] if len(splitList) > 1 else None
        originalFilePath = os.path.join(os.getcwd(), inputString)
        if os.path.exists(inputString):
            if directoryName:
                directoryPath = os.path.join(os.getcwd(), directoryName)
                if not os.path.exists(directoryPath):
                    os.makedirs(directoryPath)
                    newFilePath = os.path.join(directoryPath, fileName)
                    os.rename(originalFilePath, newFilePath)
                    print(f"File '{fileName}' stored in directory '{directoryName}'")
                else:
                    newFilePath = os.path.join(directoryPath, fileName)
                    os.rename(originalFilePath, newFilePath)
                    print(f"File '{fileName}' stored in directory '{directoryName}'")
        else:
             print(f"File '{fileName}' does not exist in the directory '{directoryName}'")       


    def m_ReadDirectory(self):
        for filename in os.listdir("."):
            if os.path.isfile(filename):
                self.m_SplitAndStore(filename, "_")    

    def organize(self):
        self.m_ReadDirectory()


class c_GradeMain:
    def __init__(self,totalPoints=100):
        self.totalPoints=totalPoints
        self.listOfStudents= self.m_StudentsDict()
        self.listOfStudentsGraded= set()
        self.feedback={}

    def m_StudentsDict(self):
        dict={}
        for name in os.listdir("."):
            if os.path.isdir(os.path.join(".", name)):
                dict[name]=c_student(name)
        return dict

    def m_getStudent(self,name):
        return self.listOfStudents[name]

    


class c_student:
    def __init__(self,name,startPoints=100,submitLog="submit.log",gradeFile="grade.file",duedate="Thursday, February 2, 2023 11:59:59 PM EST"):
        self.name = name
        self.totalPoints = startPoints
        self.submitLog=submitLog
        self.feedbackFile=gradeFile
        self.feedback = self.m_InitFeedback()
        self.m_CheckSubmissionTime(duedate)

    def m_InitFeedback(self):
        return self.m_FeedbackHeader(os.path.join(os.getcwd(),self.name,self.submitLog)) + "Grade: ??\n\nFeedback:-\n" 
 

    def m_FeedbackHeader(self,filePath) -> str:
        with open(filePath, 'r') as file:
            lines = file.readlines()[:3]
        return "".join(lines)



    def _ExtractDate_(self,filePath):
        with open(filePath, 'r') as file:
            file_content = file.read()

        match = re.search(r'Date Submitted: (.*)', file_content)
        dateSubmitted = match.group(1)
        return dateSubmitted
    
 

    def _CheckSubmissionTime_(self,student,dueDate):
        timeSubmission= self._ExtractDate_(os.path.join(os.getcwd(), student,self.submitLog))
        timeSubmission = parser.parse(timeSubmission)
        timeDue = parser.parse(dueDate)
        timeDiffernce = timeDue - timeSubmission
        second = timeDiffernce.total_seconds()
        hours, remainder = divmod(abs(second), 3600)
        minutes, seconds = divmod(remainder, 60)

        if second < 0:

            if hours >= 1 and hours < 24:
                self.totalPoints-=10
                self.feedback+= f"{-10:<6} Late Submission:  {int(hours):02d}hours {int(minutes):02d}minutes {int(seconds):02d}seconds\n"
            elif hours >= 24 and hours < 48:
                self.totalPoints-=20
                self.feedback += f"{-20:<6} Late Submission: {int(hours):02d}hours {int(minutes):02d}minutes {int(seconds):02d}seconds\n"
            elif hours >= 48:
                self.totalPoints=0
                self.feedback += f"{0:<6} Late Submission:  {int(hours):02d}hours {int(minutes):02d}minutes {int(seconds):02d}seconds\n"
    
    def m_CheckSubmissionTime(self,duedate="Thursday, February 2, 2023 11:59:59 PM EST"):
        self._CheckSubmissionTime_(self.name,duedate)



    def m_CreateGradeFile(self):
        with open(os.path.join(os.getcwd(),self.name,self.feedbackFile), 'w') as file:
            file.write(self.feedback)



    def _Decompress_(self,student,filename):
        currentWorkingDir = os.getcwd()
        path =os.path.join(os.getcwd(), student)
        print(f'Changing working directory to {path}')
        os.chdir(path)

        with zipfile.ZipFile(filename, "r") as file:
            file.extractall()

        print(f'Changing working directory back to {currentWorkingDir}')
        os.chdir(currentWorkingDir)    
    


    def m_Decompress(self,filename):
        if os.path.isfile(os.path.join(os.getcwd(), self.name,filename)):
            self._Decompress_(self.name,filename)
        else:
            ipt="y"
            while(ipt!="q"):
                for file in os.listdir("."):
                    if os.path.isfile(file):
                        print(file)
                ipt=input("Give a file name[q to exit]: ")
                if ipt == "q":
                    self.feedback+= f"{filename} does not exist\n"
                elif os.path.isfile(os.path.join(os.getcwd(), self.name,ipt)):
                    self._Decompress_(self.name,ipt)
                    self.feedback+= f"Bad file name: {ipt} found instead of {filename}\n"
                    ipt="q"
                else:
                    print("Try Again!!")



class c_GradeLab5():
    def __init__(self,GradeMain:c_GradeMain,filesReq="lab5_1.c lab5_2.c lab5_3.c",zipFile="lab5.zip"):
        self.GradeMain = GradeMain
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


    def m_gradeLab5(self,name):
        student = self.GradeMain.listOfStudents[name]
        currentWorkingDir = os.getcwd()
        path =os.path.join(os.getcwd(),name)
        # print(f'Changing working directory to {path}')
        os.chdir(path)
        self.m_CheckQuestion1(student)
        self.m_CheckQuestion2(student)
        self.m_CheckQuestion3(student)
        self.m_createFeedbackFile(student)
        # print(f'Changing working directory back to {currentWorkingDir}')
        os.chdir(currentWorkingDir)


    def m_createFeedbackFile(self,student):
        with open(student.feedbackFile, "w+") as f:
            f.write(student.feedback)


    def m_compileTestingExe(self,output,input):
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
        student.feedback+= f"\nPart-1 Reverse the string\n"
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

    def m_CheckQuestion2(self,student):
        student.feedback+= f"\nPart-2 Reverse the string[*pointers]\n"
        filename = self._CheckFile_(student,self.filesReq[1])
        if( filename != False):

            output = "Question2"
            if(self.m_compileCfile(["gcc", filename, "-o", output])):
                subprocess.run(["less", f"{filename}"])
                while(1):
                    grade = input("Grade[?/5]: ")
                    if grade.isdigit():
                        grade = int(grade)
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

    def m_CheckQuestion3(self,student):
        student.feedback+= f"\nPart-3 Modifying split function accept 1 array, 2 int* and return int*\n"
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
        



class c_Shell():
    def __init__(self):
        if(self.initalizer()== False):
            print("Couldn't initalize the script")
            exit(0)
        c_DirOrganizer().organize()
        self.GradeMain = c_GradeMain()
        self.loadProgress()
        self.assignmentsToGrade= len(self.GradeMain.listOfStudents)
        self.grade=c_GradeLab5(self.GradeMain)
        self.menu()

    def initalizer(self):
        print(f"Current Working Directory: {os.getcwd()}")
        print("Assignments available:-")
        for file in os.listdir("."):
            if os.path.isdir(file):
                print(file, end=" ")
        print()
        while(1):
                ipt=input("Which Assignment would you like to grade [q to exit]: ")
                if ipt == "q":
                    return False
                elif os.path.isdir(ipt):
                    os.chdir(ipt)
                    self.assignmentGraded = ipt
                    return True
                else:
                    print("Try Again!!")
    
    def loadProgress(self):
        try:
            with open("students.graded", "r") as f:
                data = json.load(f)
            self.GradeMain.listOfStudentsGraded = set(data)
        except:
            self.GradeMain.listOfStudentsGraded = set()

    def saveProgress(self):
        with open("students.graded", "w+") as f:
            json.dump(list(self.GradeMain.listOfStudentsGraded), f)

    def _gradeHelper_(self,name,assignmentsGraded):
            print(f"Graded : {assignmentsGraded}")
            print(f"Number of assignments left {self.assignmentsToGrade - assignmentsGraded}")
            while True:
                userInput = input(f"Grade {name} [(y)es/(n)o/(q)uit]: ")
                match userInput.lower():
                    case "y":
                        self.grade.m_gradeLab5(name)
                        break
                    case "n":
                        print("No")
                        break
                    case "q":
                        print("quit")
                        break
                    case _:
                        print("try again")
                        continue
            self.GradeMain.listOfStudentsGraded.add(name)
            self.saveProgress()


    def m_shellFreshGrade(self):
        self.GradeMain.listOfStudentsGraded.clear()
        assignmentsGraded=len(self.GradeMain.listOfStudentsGraded)
        for name in self.GradeMain.listOfStudents.keys():
            self._gradeHelper_(name,assignmentsGraded)
            assignmentsGraded+=1
            

    def m_shellGrade(self):
        assignmentsGraded=len(self.GradeMain.listOfStudentsGraded)
        for name in self.GradeMain.listOfStudents.keys():
            if name not in self.GradeMain.listOfStudentsGraded:
                self._gradeHelper_(name,assignmentsGraded)
                assignmentsGraded+=1


    def menu(self):
        assignmentsGraded=len(self.GradeMain.listOfStudentsGraded)
        print(f"Number of Students to grade : {self.assignmentsToGrade}")
        print(f"Number of assignments graded: {assignmentsGraded}")
        print(f"------------------------------------------------------------------------------")
        print(f"Options:-")
        print(f"Grade   - Start grading students")
        print(f"Mail    - All the students there grade")
        print(f"Tab     - Tabulate all the grade")
        print(f"Exit    - Do nothing")
        while True:
                userInput = input(f"Enter Action>")
                match userInput.lower():
                    case "grade":
                        print(f"------------------------------------------------------------------------------")
                        self.m_shellStruct()
                        break
                    case "mail":
                        print(f"------------------------------------------------------------------------------")
                        break
                    case "tab":
                        print("Feature under way")
                        break
                    case "exit":
                        break
                    case _:
                        print("try again")
                        continue



    def m_shellStruct(self):
        assignmentsGraded=len(self.GradeMain.listOfStudentsGraded)
        if (assignmentsGraded !=0):
            while True:
                    print(f"Number of assignments already graded: {assignmentsGraded} out of {self.assignmentsToGrade}")
                    userInput = input("Do you want to start Grading form where you left? [(y)es/(n)o/(q)uit]: ")
                    match userInput:
                        case "y":
                            self.m_shellGrade()
                            break
                        case "n":
                            self.m_shellFreshGrade()
                            break
                        case "q":
                            print("quit")
                            break
                        case _:
                            print("try again")
                            continue
        else:
            self.m_shellFreshGrade()

            


            




# class c_Assignments(c_Shell):
#     def __init__(self):
#         self.Lab5 = c_GradeLab5(self.GradeMain)


                

def main():
    ################################################################
    #Pre-Req
    currentWorkingDir = os.getcwd()
    path =sys.argv[1]
    # print(f'Changing working directory to {path}')
    os.chdir(path)
    ################################################################



    c_Shell()
    # grade = c_GradeMain()
    # grade_lab5 = c_GradeLab5(grade,zipFile=None)
    # grade_lab5.m_CheckQuestion1("ss5278")
    # grade_lab5.m_CheckQuestion2("ss5278")
    # grade_lab5.m_CheckQuestion3("ss5278")
    # print(grade.m_getStudent("ss5278").feedback)

    ################################################################
    #Post-Req
    # print(f'Changing working directory back to {currentWorkingDir}')
    os.chdir(currentWorkingDir)
    ################################################################

if __name__ == "__main__":
    main()
