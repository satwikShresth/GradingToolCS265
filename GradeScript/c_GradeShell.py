from c_AssignmentTrack import c_AssignmentTrack
from c_GradeMain import c_GradeMain
from c_TerminalUserInterface import c_termianlUserInterface


class c_GradeShell(c_AssignmentTrack):
    def __init__(self,uI: c_termianlUserInterface, assignmentName):
        self.s_assignmentName: str = assignmentName
        self.o_uI= uI
        self.m_initalize()

    def m_initalize(self):
        pass

    def m_grade(self, name):
        pass