from PIL import Image
import numpy as np
import requests
from bs4 import BeautifulSoup
from urllib.request import urlopen
from urllib.request import Request
import string
import sys

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
        
        # Horizontally combine
        self.combine()

    def combine(self):
        
        list_im = ['1.jpg', '2.jpg', '3.jpg']
        imgs    = [ Image.open(i) for i in list_im ]
        # pick the image which is the smallest, and resize the others to match it (can be arbitrary image shape here)
        min_shape = sorted( [(np.sum(i.size), i.size ) for i in imgs])[0][1]
        imgs_comb = np.hstack( (np.asarray( i.resize(min_shape) ) for i in imgs ) )

        # save that beautiful picture
        imgs_comb = Image.fromarray( imgs_comb)
        imgs_comb.save( 'Trifecta.jpg' )    

        # for a vertical stacking it is simple: use vstack
        imgs_comb = np.vstack( (np.asarray( i.resize(min_shape) ) for i in imgs ) )
        imgs_comb = Image.fromarray( imgs_comb)
        imgs_comb.save( 'Trifecta_vertical.jpg' )