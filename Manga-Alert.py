import bs4
import requests
from test import Test

filename = "list.csv"
test = Test(filename)
test.run()

if __name__ == "__main__":
    print("Tests : OK")
    website_url = "http://www.japscan.cc/mangas/"
    list_path = "list.csv"

    response = requests.get(website_url)
    #Get the data from the url in text format
    data = response.text


    
