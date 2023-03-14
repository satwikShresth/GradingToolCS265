import os
import hashlib
import json,pickle
from c_Grader import c_Grader
from c_TerminalUserInterface import c_termianlUserInterface

PROFILE = "/home/ss5278/GradeScript/graderProfiles"

class c_Authenticator:
    def __init__(self,uI:c_termianlUserInterface,keyFile = ".gradeKey"):
        self.o_uI = uI
        self.keyFile = keyFile
        self.d_listOfGrader:dict[str:c_Grader]
        self.m_Initialize()
        self.s_tabFileName = "grades.tab"


    def m_Initialize(self):
        self.grader = os.getcwd().split("/")[2]
        self.m_loadKeyFile()
        self.d_listOfStudents = dict(sorted(self.d_listOfStudents.items()))

    def m_getGrader(self, name):
        return self.d_listOfGrader[name]

    def m_createNewGrader(self):

    def m_loadKeyFile(self):
        home_dir = os.path.expanduser("~")
        key_file_path = os.path.join(home_dir,".gradeKey")
        try:
            with open(key_file_path, "r") as key_file:
                self.gradeKey = key_file.read().strip()
                self.m_loadProfile()
        except:







    def m_saveProfile(self,name):
        try:
            with open(os.path.join(PROFILE,f"{name}.profile"), "wb+") as f:
                pickle.dump(self.d_listOfStudents[name],f)
        except Exception as e:
            instructions = [f"Error:", f"{e}"]
            options = [f"Continue"]
            self.o_uI.m_terminalUserInterface(options, instructions)
            

    def m_loadProfile(self):
        try:
            with open(os.path.join(PROFILE,f"{self.grader}.profile"), "rb") as f:
                self.grader = pickle.load(f)
            self.authenticate(self.grader.hashKey)


        except Exception as e:
            instructions = [f"Error:", f"{self.grader}.profile not found in database","Create new profile ?"]
            options = [f"Continue","Skip"]
            response = self.o_uI.m_terminalUserInterface(options, instructions)
            if response == options[0]:
                self.d_listOfStudents[self.grader] = c_Grader(self.grader)
                with open(os.path.join(PROFILE,f"{self.grader}.profile"), "wb+") as f:
                    pickle.dump(self.d_listOfStudents[self.grader],f)


    def create_user_directory(self):
        if not os.path.exists(self.home_directory):
            os.makedirs(self.home_directory)

    def save_grade_key(self):
        key_file_path = os.path.join(self.home_directory, ".gradeKey")
        with open(key_file_path, "w") as key_file:
            key_file.write(self.hash_key)

    def save_user_profile(self):
        profile = {
            "username": self.username,
            "hash_key": self.hash_key
        }
        profile_file_path = os.path.join(self.cwd, f"{self.username}_profile.json")
        with open(profile_file_path, "w") as profile_file:
            json.dump(profile, profile_file)

    def create_account(self):
        self.create_user_directory()
        self.save_grade_key()
        self.save_user_profile()
