from c_AssignmentTrack import c_AssignmentTrack
from c_GradeMain import c_GradeMain
from c_TerminalUserInterface import c_termianlUserInterface


class c_GradeShell(c_AssignmentTrack):
    def __init__(self, GradeMain: c_GradeMain, assignmentName):
        self.s_assignmentName: str = assignmentName
        self.o_uI: c_termianlUserInterface = c_termianlUserInterface()
        self.o_gradeMain: c_GradeMain = GradeMain
        self.m_initalize()

    def m_initalize(self):
        pass

    def m_grade(self, name):
        pass
