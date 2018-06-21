from PIL import Image
import requests
from bs4 import BeautifulSoup

class PageCombiner():
    def __init__(self, _name, _chapter, _url):
        print("Combining chapter's image...")

        # Attributes
        self.name = _name
        self.chapter = _chapter
        self.url = _url
        self.response = requests.get(self.url, stream = True)

        # Check if we got a response from the url
        if(self.response.status_code == 200):
            self.data = self.response.text
            self.soup = BeautifulSoup(self.data, 'lxml')

            # Count how mane pages the chapter has
            self.pageCount = self.countPage()
        
            # Start the process
            self.run()

    def countPage(self):
        print("Counting pages..")

        # List all the <a> tags with attribute class = "pagi"
        content = self.soup.find_all('a', {'class' : 'pagi'})
        for pageNb in content:
            
            # Get <a> tag content until the last one
            lastPage = int(pageNb.get_text())
        return lastPage
    
    # This function purpose is to combine all the chapter's page into a single one
    def run(self):
        
        if( self.response.status_code == 200 ):

            print("The chapter " + str(self.chapter) + " contain " + str(self.pageCount) + " pages")

            soup = BeautifulSoup(self.data, 'lxml')

            # Find how many pages there are

            # Find src attribute of <img> tag

        else:
            print("The url send an error code : " + str(self.response.status_code))
