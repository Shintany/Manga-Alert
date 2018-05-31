import os.path
import socket

class Test():
    def __init__(self, filePath):
        print("\t---Tests---")
        self.path = filePath

    def run(self):
        try:
            self.fileExist()
            self.internetAccess()
        except Exception as error:
            print(repr(error))

    def fileExist(self):
        if os.path.exists(self.path):
            print("File exist : OK")
        else:
            print("File exist : Error")
            raise Exception('File was not found')
    
    def internetAccess(self):
        str_google = "www.google.com"
        try:
            socket.gethostbyname(str_google)
            print("Internet access : OK")
        except OSError as error:
            print("Internet access : Error")
            print("No internet access...")
            raise Exception(error)

        