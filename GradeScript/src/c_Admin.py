import os
import hashlib
import json
import pickle
from .c_Grader import c_Grader
from .c_TerminalUserInterface import c_termianlUserInterface
from .c_Mail import c_Mail

PROFILE = "/home/ss5278/GradeScript/graderProfiles"


class c_Authenticator:
    def __init__(self):
        self.d_listOfGrader:dict
        self.instructions