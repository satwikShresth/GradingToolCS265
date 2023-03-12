import copydetect,os
from c_GradeMain import c_GradeMain

class c_CodeChecker:
    def __init__(self,o_gradeMain:c_GradeMain):
        self.o_gradeMain = o_gradeMain
        self.fingerprints:dict={}
        self.detector:copydetect.CopyDetector = copydetect.CopyDetector(force_language="c",extensions=["c"],display_t=0.5,autoopen=False)
        self.m_initialzeFingerprint()

    def m_initialzeFingerprint(self):
        path = os.getcwd()
        fingerprintdict=[]
        for name in self.o_gradeMain.d_listOfStudents.keys():
            filename = os.path.join(path,name)
            for files in os.listdir(filename):
                if files.endswith(".c"):
                    cFile = os.path.join(filename,files)
                    self.detector.add_file(filename=cFile,type="testref")
                    fingerprintdict += [copydetect.CodeFingerprint(cFile,5,2,language="c")]
            self.fingerprints[name] = fingerprintdict

    def m_generateReport(self):
        self.detector.run()
        self.detector.generate_html_report()