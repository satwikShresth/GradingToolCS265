import os
import hashlib
import pickle
from .hiddenMethods import generateHashKey
from .c_Grader import c_Grader,permission
from .c_TerminalUserInterface import c_termianlUserInterface
from .c_Mail import c_Mail

PROFILE = "/home/ss5278/GradeScript/graderProfiles"


class c_Authenticator:
    def __init__(self, keyFile=".gradeKey"):
        self.keyFile = keyFile
        self.authentication = False
        self.instructionsGranted="1. Create a file .gradeKey in your home directory\n2. Copy the hash key below into the file\n-----------------------copy-below-----------------------\n\n"
        self.instructionsDenied="You have been denied for Gradekey"
        self.mail = c_Mail(s_subject="Instructions for your CS265 grader tool")
        self.m_Initialize()

    def m_Initialize(self):
        grader = os.getcwd().split("/")[2]
        usrKey = self.m_loadKeyFile()
        self.grader,profileKey  = self.m_loadProfile(grader)

        if not usrKey and not profileKey:
            print("New User: ",self.grader)
            if input("Create a new profile!! [y]/n ").lower == "n":
                SystemExit()
            else:
                homeDir = os.path.expanduser("~")
                self.m_createNewGrader(homeDir.split("/")[2])
        elif usrKey and not profileKey :
            print("This incident will be reported!!")
            SystemExit()
        elif not usrKey and profileKey:
            print("Please check your email for instructions!")
            if input("Do you want to resend the email with instructions? y/[n]").lower() == "y":
                self.m_sendInstructions(self.grader)
        elif usrKey and profileKey:
            if self.authenticate(usrKey,profileKey):
                self.authentication = True
            else:
                print("Autentication Failed")
                if input("Do you want to resend the email with instructions? y/[n]").lower() == "y":
                    self.m_sendInstructions(self.grader)
    

    def m_sendInstructions(self,grader):
        if grader.status == permission.GRANTED:
            self.mail.m_sendInstructions(self.instructionsGranted,self.grader.hashKey,self.grader.username) # type: ignore
        elif grader.status == permission.DENIED:
            self.mail.m_sendInstructions(self.instructionsGranted,self.grader.hashKey,self.grader.username) # type: ignore
        elif grader.status == permission.REQUESTED:
            print("Please Wait till we complete your request")

    def authenticate(self,usr_hashKey,profile_hashKey):
        return usr_hashKey == profile_hashKey


    def m_createNewGrader(self,usrname):
        print("New User: ",usrname)
        name = input("Enter a name: ")
        password = input("Enter a password: ")
        keyData = f"{usrname}:{name}:{password}".encode("utf-8")
        hashKey = generateHashKey(usrname,name,password)
        self.grader = c_Grader(usrname,name,hashKey)
        self.m_saveProfile(self.grader)
        print("Your request has been sent to the Admin")
        input("enter any key to continue...")

    def m_saveProfile(self, obj:c_Grader):
        try:
            with open(os.path.join(PROFILE, f"{obj.username}.profile"), "wb+") as f:
                pickle.dump(obj, f)
        except Exception as e:
            print(f"Error:", f"{e}")
            input("press anything to continue...")


    def m_loadKeyFile(self):
        gradeKey = False
        homeDir = os.path.expanduser("~")
        keyFilePath = os.path.join(homeDir, ".gradeKey")
        try:
            with open(keyFilePath, "r") as key_file:
                gradeKey = key_file.read().strip()
        except:
            print(".graderKey file not found")
            input("press anything to continue...")
        
        return gradeKey

    def m_loadProfile(self,grader):
        try:
            with open(os.path.join(PROFILE, f"{grader}.profile"), "rb") as f:
                grader = pickle.load(f)
            return (grader,grader.hashKey)
        
        except:
            print(f"{self.grader} profile not found")
            input("press anything to continue...")
        
        return (False,False)
    
    def m_createDic(self):
        self.d_graders = {}
        for files in os.listdir(PROFILE):
            name = files.split(".")[0]
            self.d_graders[name],hashKey = self.m_loadProfile(name)

    def m_admin(self,uI:c_termianlUserInterface):
        self.m_createDic()
        grader:c_Grader = uI.m_selectGraders(self.d_graders)
        instructions = [f'{grader.name} ({grader.username}) has requested for permission']
        options= ["Grant Permission","Deny","Go back"]
        selected = uI.m_terminalUserInterface(options,instructions)
        if selected is options[0]:
            grader.status = permission.GRANTED
        elif selected is options[1]:
            grader.status = permission.DENIED
        self.m_saveProfile(grader)
        uI.m_end()
        self.m_sendInstructions(grader)
        uI.m_restart()
