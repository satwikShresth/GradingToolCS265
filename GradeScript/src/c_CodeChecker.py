import copydetect,os
import mosspy
from c_GradeBook import c_GradeBook

class c_CodeChecker:
    def __init__(self,o_gradeMain:c_GradeBook):
        self.o_gradeMain = o_gradeMain
        os.mkdir("AssignmentReport")
        self.reportDir = os.path.join(os.getcwd(),"AssignmentReport")
        self.detector:copydetect.CopyDetector = copydetect.CopyDetector(out_file=f"{self.reportDir}//CCReport.html",force_language="c",extensions=["c"],noise_t=3,guarantee_t=4,display_t=0.6)
        self.moss = mosspy.Moss(30768978, "c")
        self.m_initialzeFingerprint()

    def m_initialzeFingerprint(self):
        path = os.getcwd()
        for name in self.o_gradeMain.d_listOfStudents.values():
            filename = os.path.join(path,name)
            for files in os.listdir(filename):
                if files.endswith(".c"):
                    cFile = os.path.join(filename,files)
                    self.detector.add_file(filename=cFile,type="testref")
                    self.moss.addFile(cFile,name)
        try:
            for files in os.listdir(os.path.join(path,"references")):
                if files.endswith(".c"):
                    cFile = os.path.join("references",files)
                    self.detector.add_file(filename=cFile,type="ref")
                    self.moss.addFile(cFile)
        except:
            pass

    def m_generateMossReport(self):
        url = self.moss.send(lambda file_path, display_name: print('*', end='', flush=True))
        self.moss.saveWebPage(url, os.path.join(self.reportDir,"MossReport.html"))
        mosspy.download_report(url, os.path.join(self.reportDir,"MossReport"), connections=8, log_level=10, on_read=lambda url: print('*', end='', flush=True))
    def m_generateCCReport(self):
        self.detector.run()
        self.detector.generate_html_report()