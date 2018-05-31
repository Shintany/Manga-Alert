import os.path

class Test():
    def __init__(self, filePath):
        print("---Tests---")
        self.path = filePath

    def run(self):
        try:
            self.fileExist()
        except Exception as error:
            print(repr(error))


    def fileExist(self):
        if os.path.exists(self.path):
            print("File exist : OK")
        else:
            print("File exist : Error")
            raise Exception('File was not found')