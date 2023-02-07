import os

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