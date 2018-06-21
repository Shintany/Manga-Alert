from PIL import Image
import requests
from bs4 import BeautifulSoup
from urllib.request import urlopen
from urllib.request import Request
import string

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

            # Find id attribute of <img> tag with "image" as value
            img_soup = self.soup.find('img', {'id' : 'image'})

            # Adding headers otherwise, we're getting kicked out of the website
            user_agent = 'Mozilla/5.0 (iPhone; CPU iPhone OS 5_0 like Mac OS X) AppleWebKit/534.46'

            # Count the number of zero in src
            # It will allow us to know the format url
            zeroCount = img_soup['data-img'].count('0')
    
            # Reformat manga name
            formatted_name = ""
            word_list = self.name.split(" ")
            for word in word_list:
                if not word[0].isupper():

                    # Convert lower to upper
                    upper_letter = word[0].upper()
                    if len(word) > 1:
                        word = upper_letter + word[1:]
                    else:
                        word = upper_letter
                formatted_name = formatted_name + "-" + word
            
            # Deleting the first "-"
            formatted_name = formatted_name[1:]

            # src format : https://cdn.japscan.cc/lel/Manga-Name/chapter/img_soup['src]
            image_url_base = "https://cdn.japscan.cc/lel/" + formatted_name + "/" + str(self.chapter) + "/"

            # Initialize counter
            for i in range(1, self.pageCount + 1, 1):

                img_name = ""
                # Adding as much zero as the first url had
                for j in range(0, zeroCount):
                    img_name = img_name + "0"
                img_name = img_name + str(i) + ".jpg"
                image_url = image_url_base + img_name

                print(image_url)
                print(img_soup['src'])

                # Download image
                img = open(img_name, 'wb')
                img.write( urlopen( Request(image_url, headers={'User-Agent': user_agent})).read() )
                img.close()

        else:
            print("The url send an error code : " + str(self.response.status_code))
