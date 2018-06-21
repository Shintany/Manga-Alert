from PIL import Image
import requests
from bs4 import BeautifulSoup
from urllib.request import urlopen
from urllib.request import Request

class PageCombiner():
    def __init__(self, _name, _chapter, _url):

        # Attributes
        self.name = _name
        self.chapter = _chapter
        self.url = _url
        self.response = requests.get(self.url, stream = True)
        self.data = ""

        # Check if we got a response from the url
        if(self.response.status_code == 200):
            self.data = self.response.text
            self.soup = BeautifulSoup(self.data, 'lxml')

            # Count how mane pages the chapter has
            self.pageCount = self.countPage()
        
            # Start the process
            self.run()

    def countPage(self):

        # List all the <a> tags with attribute class = "pagi"
        content = self.soup.find_all('a', {'class' : 'pagi'})
        for pageNb in content:

            # Get <a> tag content until the last one
            lastPage = int(pageNb.get_text())
        return lastPage
    
    # This function purpose is to combine all the chapter's page into a single one
    def run(self):
        
        if( self.response.status_code == 200 ):

            soup = BeautifulSoup(self.data, 'lxml')

            # Initialize counter
            i = 1
            while i <= self.pageCount:

                # Find id attribute of <img> tag with "image" as value
                img_soup = soup.find('img', {'id' : 'image'})
                print(img_soup['src'])

                # Download image
                user_agent = 'Mozilla/5.0 (iPhone; CPU iPhone OS 5_0 like Mac OS X) AppleWebKit/534.46'
                img = open(img_soup['data-img'], 'wb')
                img.write( urlopen( Request(img_soup['src'], headers={'User-Agent': user_agent})).read() )
                img.close()
                i = i + 1

        else:
            print("The url send an error code : " + str(self.response.status_code))
