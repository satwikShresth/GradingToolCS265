import os,shutil
import subprocess
import sys,re,json
from .c_TerminalUserInterface import c_termianlUserInterface
from .c_AssignmentTrack import c_AssignmentTrack
from .c_Student import c_Student


class c_GradeCommon(c_AssignmentTrack):
    def __init__(self,uI: c_termianlUserInterface,jsonData):
        self.o_uI = uI
        self.m_gradeSetup(jsonData)
        self.compilationError=False

    def m_gradeSetup(self,jsonData):
        try:
            self.jsonData = jsonData
            self.assignmentName = jsonData["assignmentName"]
            self.dueDate = jsonData["dueDate"]
            self.zipFile = jsonData["zipFile"]
            self.filesReq = jsonData["filesReq"]
            self.checkMemoryLeak = jsonData["checkMemoryLeak"]
            self.checkFunctions = jsonData["checkFunctions"] 
            self.d_questions:dict = jsonData["Questions"]
            self.testFilesReq = jsonData["testFileReq"]

        except Exception as e:
            instructions = [f"Error:", f"{e}"]
            options = [f"Continue"]
            self.o_uI.m_terminalUserInterface(options, instructions)
            sys.exit(0)


    def m_gradeHelper(self,student:c_Student,output,question):
        title = question["title"]
        student.s_initialFeedback += f"-----------------------------------------------------------------------\n"
        student.s_initialFeedback += f"{output}:{title}\n"
        student.s_initialFeedback += f"-----------------------------------------------------------------------\n"
        if question["language"].lower() == "c":
            self.m_checkQuestionInC(student,output,question)
        student.s_feedback += student.s_initialFeedback
        student.s_initialFeedback = ""
        


    def m_grade(self,student:c_Student):
        self.compilationError = False
        name = student.s_name
        student.m_CheckSubmissionTime(self.dueDate,self.assignmentName)
        currentWorkingDir = os.getcwd()
        path = os.path.join(os.getcwd(), name)
        # print(f'Changing working directory to {path}')
        os.chdir(path)

        if self.testFilesReq != False:
            for files in self.testFilesReq:
                shutil.copy(os.path.join(currentWorkingDir,files),os.path.join(path,files))

        for key,values in self.d_questions.items():
            if self.m_Decompress(student,self.zipFile) and self.zipFile.lower() != "none":
                self.m_gradeHelper(student,key,values)
            else:
                student.s_feedback += f"-----------------------------------------------------------------------\n"
                student.s_feedback += f"No zipFile found\n"
                student.s_feedback += f"-----------------------------------------------------------------------\n"
                student.f_grade = 0
            self.m_finalizeGrade(student)
            self.m_createFeedbackFile(student.s_feedbackFile, student.s_feedback)
            self.m_gradedReport(student)
            student.m_registerGrade()

        # print(f'Changing working directory back to {currentWorkingDir}')
        os.chdir(currentWorkingDir)


    def m_testQuestion(self, student: c_Student, execFile,testString):
        pointsDeduct = 0
        for test in testString:
            inputType = test["inputType"]
            input = test["input"]
            expected = test["expected"]
            points = test["points"]
            pointDivided = int(points/len(expected))
            try:
                if inputType == "stdin":
                    process = subprocess.getstatusoutput(f'printf "{input}"| ./{execFile} | iconv -f iso-8859-1 -t utf-8//IGNORE')
                elif inputType == "sysarg":
                    process = subprocess.getstatusoutput(f'./{execFile} {input} | iconv -f iso-8859-1 -t utf-8//IGNORE')
            except Exception as e:
                student.s_initialFeedback += f" {-points:<6}Error: {e}\n"
                student.s_initialFeedback += f"-----------------------------------------------------------------------\n"
                return -(points)
                
            if process[0] != 0:
                student.s_initialFeedback += f" {-points:<6}Error:{process[1]}\n"
                student.s_initialFeedback += f"-----------------------------------------------------------------------\n"
                return -(points)
            self.output = process[1]
            if type(expected) == list:
                self.answerCheck = []
                self.m_testOutput(expected)
                if(len(self.answerCheck) >= 1):
                    pointz = 0
                    pointz -= pointDivided*len(self.answerCheck) if pointsDeduct >5 else 5
                    output = f"\n {'':23}-> ".join(self.output.split("\n"))
                    student.s_initialFeedback += f" {pointz:<6} Failed Test     -> {input}\n"
                    student.s_initialFeedback += f" {'':6} Input type      -> {inputType}\n"
                    student.s_initialFeedback += f" {'':6} Desired output  -> {expected}\n"
                    student.s_initialFeedback += f" {'':6} Your ouput      -> {output}\n"
                    student.s_initialFeedback += f"-----------------------------------------------------------------------\n"
            self.output = ""
            pointsDeduct += points
        if (pointsDeduct == 0):
            student.s_initialFeedback += f"{'':6} All test strings passed\n"
            student.s_initialFeedback += f"-----------------------------------------------------------------------\n"
        return pointsDeduct
    

    def m_testOutput(self,expected):
        for input in expected:
            if type(input) == list:
                self.m_testOutput(input)
            else:
                if (input not in self.output):
                    self.answerCheck.append("Failed")
                    break
                else:
                    self.output = self.output.replace(input,"Passed",1)
        return True
    
#--------------------------------------------------------------------------------------------------------------------------------------
    def m_divideQuestions(self,fileContent,count,answers):
        for idx,line in enumerate(fileContent):
            if re.match(r".*q.*\d.*", line.lower()) and idx != 0: 
                return self.m_divideQuestions(fileContent[idx:],count+1,answers)
            elif idx == 0:
                answers[count] = [line]
            else:
                answers[count].append(line)
        return answers
    
    def m_checkQuestionInBash(self, student: c_Student,execFile,question):
        points = 0
        studentCurrentFilenames = []
        totalPoints = question["totalPoints"]
        testString = question["testStrings"]
        filesReq = question["file"]

        if type(filesReq) == str:
            filesReq = [filesReq]
        for file in filesReq:
            if file in student.ls_filenames:
                actualFilename = self._CheckFile_(student,student.ls_filenames[file])
            else:
                actualFilename = self._CheckFile_(student,file)
            studentCurrentFilenames.append(actualFilename)
            student.ls_filenames[file] = actualFilename

        if  False not in studentCurrentFilenames:
            fileContent = self.m_filesToStringList(studentCurrentFilenames)
            answers ={}
            answers = self.m_divideQuestions(fileContent,0,answers)

            testString = None
        else:
            student.s_initialFeedback += f" {-totalPoints:<6} Required File Missing"
            student.f_grade -= totalPoints
#--------------------------------------------------------------------------------------------------------------------------------------
    
    def m_checkQuestionInC(self, student: c_Student,execFile,question):
        points = 0
        studentCurrentFilenames = []
        totalPoints = question["totalPoints"]
        testString = question["testStrings"]
        filesReq = question["file"]

        if type(filesReq) == str:
            filesReq = [filesReq]
        for file in filesReq:
            if file in student.ls_filenames:
                actualFilename = self._CheckFile_(student,student.ls_filenames[file])
            else:
                actualFilename = self._CheckFile_(student,file)
            studentCurrentFilenames.append(actualFilename)
            student.ls_filenames[file] = actualFilename

        if  False not in studentCurrentFilenames:
            proc = ["gcc"]
            proc += studentCurrentFilenames
            proc +=["-o", execFile]
            result = self.m_compileCfile(proc)
            if (result == True):
                pointDeducted = self.m_testQuestion(student,execFile,testString)
                points += pointDeducted
            else:
                points -= 10
                self.compilationError = True
                student.s_initialFeedback += f" {-5:<6} Compilation Error: {result}"
            fileContent = self.m_filesToStringList(studentCurrentFilenames)
            feedback = self.m_autoCheck(student,execFile,testString[0],fileContent)
            self.m_regrade(student,studentCurrentFilenames,proc,fileContent,feedback,testString,[int(points), int(totalPoints)])
            testString = None
        else:
            student.s_initialFeedback += f" {-totalPoints:<6} Required File Missing"
            student.f_grade -= totalPoints
#--------------------------------------------------------------------------------------------------------------------------------------
    def m_regrade(self, student: c_Student,studentCurrentFilenames,proc,fileContent,feedback,testString,points):
        initalFeedback = student.s_initialFeedback.splitlines()
        exefilename = proc[-1]
        
        temp = self.o_uI.m_feedbackForm(fileContent + initalFeedback+feedback)
        if temp != None:
            feedback+=temp

        while True:
            instructions = initalFeedback + [exefilename,
            f"Student : {student.s_name}",
            f"Grade   : {points[1]+points[0]}/{points[1]}", "Select an option:"]
            options = ["Edit File", "Recompile", "Regrade", "Continue"]
            selectedData = self.o_uI.m_terminalUserInterface(options, instructions)
            if (selectedData == options[0]):
                super().m_selectFileAction(student,"edit",studentCurrentFilenames)
            elif (selectedData == options[1]):
                output = self.m_compileCfile(proc)
                if (output):
                    self.o_uI.m_terminalUserInterface(["Continue"], "Compilation Successful")
                    self.compilationError=False
                else:
                    self.compilationError=True
                    self.o_uI.m_terminalUserInterface(["Continue"], output)
            elif (selectedData == options[2]):
                if self.compilationError:
                    self.o_uI.m_terminalUserInterface(["Continue"], "The code did not compile","Edit the file and compile it beforehand")
                else:
                    points[0] += self.m_testQuestion(student,exefilename,testString)
            elif (selectedData == options[3]):
                if self.compilationError:
                    student.f_grade-=55
                student.f_grade+=points[0]
                student.s_initialFeedback += self.m_processFile(fileContent,feedback)
                student.s_initialFeedback +=f"\n-----------------------------------------------------------------------\n"
                break
            
    def m_filesToStringList(self, filename):
        return super().m_filesToStringList(filename)
    
    def m_autoCheck(self,student: c_Student,execFile,testString,fileContent):
        fileContent = " ".join(fileContent)
        inputType = testString["inputType"]
        input = testString["input"]
        feedback = ["Feedback:"]
        try:
            if inputType == "stdin":
                _, output = subprocess.getstatusoutput(f"printf {input} | valgrind --leak-check=full --show-leak-kinds=all ./{execFile}| iconv -f iso-8859-1 -t utf-8//IGNORE")
            elif inputType == "sysarg":
                _, output = subprocess.getstatusoutput(f"valgrind --leak-check=full --show-leak-kinds=all ./{execFile} {input}| iconv -f iso-8859-1 -t utf-8//IGNORE")
        except Exception as e:
            feedback.append(f"Error while checking memory leak: {e}\n")

        if "All heap blocks were freed -- no leaks are possible" not in output: # type: ignore
            match = re.search(r'total heap usage: (\d+) allocs, (\d+) frees', output)
            if match:
                numAllocs = int(match.group(1))
                numFrees = int(match.group(2))
                freeRatio = (numFrees/numAllocs)*100
                pointsDeduct = int((100 - freeRatio)/10)
                if pointsDeduct > 5:pointsDeduct=5
                feedback.append(f"-{pointsDeduct} points: {numFrees} out of {numAllocs} ({(numFrees/numAllocs)*100:.2f}%) Blocks freed")
                student.f_grade -=1


        for function in self.checkFunctions:
            if function not in fileContent:
                feedback.append(f"Function {function}() missing from file")
        if self.o_uI.m_checkUnreadable(fileContent) == False:
            feedback.append(f"Null character found in file")
        if "return" not in fileContent and "exit" not in fileContent:
            feedback.append(f"No exit function found")

        return feedback
    

    

    

    
