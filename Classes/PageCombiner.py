from PIL import Image
import requests
from bs4 import BeautifulSoup
from urllib.request import urlopen
from urllib.request import Request
import string
import sys
import os

class PageCombiner():
    def __init__(self, _name, _chapter, _url):

        # Attributes
        self.name = _name
        self.chapter = _chapter
        self.url = _url
        self.response = requests.get(self.url, stream = True)
        self.data = ""
        self.out_filename = ""

        # Check if we got a response from the url
        if(self.response.status_code == 200):
            self.data = self.response.text
            self.soup = BeautifulSoup(self.data, 'lxml')

            # Count how mane pages the chapter has
            self.pageCount = self.countPage()
        
            # Start the process
            self.run()

            # Horizontally combine
            self.combine()

            # Delete all temporary files
            self.deleteFile()

    def countPage(self):

        # List all the <a> tags with attribute class = "pagi"
        content = self.soup.find_all('a', {'class' : 'pagi'})
        for pageNb in content:

            # Get <a> tag content until the last one
            lastPage = int(pageNb.get_text())
        return lastPage
    
    # This function purpose is to combine all the chapter's page into a single one
    def run(self):

        print("Downloading : " + self.name)
        
        if( self.response.status_code == 200 ):

            # Adding headers otherwise, we're getting kicked out of the website
            user_agent = 'Mozilla/5.0 (iPhone; CPU iPhone OS 5_0 like Mac OS X) AppleWebKit/534.46'
    
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
                    
                    # In case if the word contains a '-' character
                    # We need to put the next letter as a capital letter
                    if '-' in  word:
                        index = word.index('-')
                        upper_letter = word[index + 1].upper()
                        word = word[0:(index + 1)] + upper_letter + word[(index + 2):]
                        
                formatted_name = formatted_name + "-" + word
            
            # Deleting the first "-"
            formatted_name = formatted_name[1:]

            # src format : https://cdn.japscan.cc/lel/Manga-Name/chapter/img_soup['src]
            image_url_base = "https://cdn.japscan.cc/lel/" + formatted_name + "/" + str(self.chapter) + "/"

            # Find id attribute of <img> tag with "image" as value
            img_soup = self.soup.find('img', {'id' : 'image'})

            # Initialize counter
            for i in range(1, self.pageCount + 1, 1):

                if i != 1:
                    # Update the page url
                    next_page_url = self.soup.find('a', {'id' : 'img_link'})
                    current_page_url = "https://www.japscan.cc" + next_page_url['href']
                    response = requests.get(current_page_url, stream=True)
                    data = response.text
                    self.soup = BeautifulSoup(data, 'lxml')
                    img_soup = self.soup.find('img', {'id' : 'image'})

                try:
                    new_page_url = image_url_base + img_soup['data-img']

                    # Download image
                    img_name = ""
                    img_name = img_name + str(i) + ".jpg"
                    img = open(img_name, 'wb')
                    img.write( urlopen( Request(new_page_url, headers={'User-Agent': user_agent})).read() )
                    img.close()
                # Ignore pub page
                except TypeError as msg:
                    print(" ")

        else:
            print("The url send an error code : " + str(self.response.status_code))

    def combine(self):

        img = Image.open('1.jpg', 'r')
        img_w, img_h = img.size
        background = Image.new('RGB', (img_w, img_h * (self.pageCount - 1)), (255, 255, 255))
        background.paste(img, (0,0))

        for i in range(2, self.pageCount):
            img = Image.open(str(i) + '.jpg')
            offset = (0, (i-1)* img_h)
            background.paste(img, offset)

        self.out_filename = self.name + '-' + str(self.chapter) + '.jpg'

        background.save( self.out_filename )

    def deleteFile(self):
        print("Deleting files...")
        for file in range(1,self.pageCount):
            os.remove(str(file) + '.jpg')
