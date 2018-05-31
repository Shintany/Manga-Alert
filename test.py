
class Test():
    def __init__(self, filePath):
        print("\t---Tests---")
        self.path = filePath

    def run(self):
        try:
            self.doesFileExist()
            self.haveInternetAccess()
            self.isWebSiteUp()
        except Exception as error:
            print(repr(error))

    def doesFileExist(self):
        import os.path
        if os.path.exists(self.path):
            print("File exist : OK")
        else:
            print("File exist : Error")
            raise Exception('File was not found')
    
    def haveInternetAccess(self):
        import socket
        str_google = "www.google.com"
        try:
            socket.gethostbyname(str_google)
            print("Internet access : OK")
        except OSError as error:
            print("Internet access : Error")
            print("No internet access...")
            raise Exception(error)

    def isWebSiteUp(self):
        import requests
        #Web site where I want to check latest release
        website_url = "http://www.japscan.cc"
        response = requests.get(website_url, stream=True)
        if response.status_code != 200:
            print("Japscan website access : Error")
            raise Exception("Japscan must be down...")
        else:
            print("Japscan website access : OK")


        