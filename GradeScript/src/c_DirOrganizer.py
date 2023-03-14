import os
from zipfile import ZipFile

class c_DirOrganizer:
    def __init__(self):
        lst = os.listdir(".")
        for files in lst:
            name, ext = os.path.splitext(files)
            if os.path.isfile(files) and "gradebook" in name and "zip" in ext:
                with ZipFile(files, "r") as file:
                    file.extractall(".")
                os.remove(files)
        lst = os.listdir(".")
        for files in lst:
            if os.path.isdir(files) and "gradebook" in files:
                target_dir = os.getcwd()
                files = os.listdir(files)
                for file in files:
                    source_path = os.path.join(files, file)
                    target_path = os.path.join(target_dir, file)
                    os.rename(source_path, target_path)
                os.remove(files)
        self.m_ReadDirectory()    



    def m_SplitAndStore(self, inputString, delimiter):
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
                    print(
                        f"File '{fileName}' stored in directory '{directoryName}'")
                else:
                    newFilePath = os.path.join(directoryPath, fileName)
                    os.rename(originalFilePath, newFilePath)
                    print(
                        f"File '{fileName}' stored in directory '{directoryName}'")
        else:
            print(
                f"File '{fileName}' does not exist in the directory '{directoryName}'")

    def m_ReadDirectory(self):
        for filename in os.listdir("."):
            if os.path.isfile(filename):
                self.m_SplitAndStore(filename, "_")