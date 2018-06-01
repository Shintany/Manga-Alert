from bs4 import BeautifulSoup
import string
import requests
from test import Test
from tools import Database
import sys

filename = "list.csv"
test = Test(filename)
test.run()

if __name__ == "__main__":
    print("Tests : OK")

    if len(sys.argv) != 2:
        print ("Argument missing...")
        print("Usage : python3 Manga-Alert.py $databasePath")
        exit()
    databasePath = sys.argv[1]

    # Filling the dictionnary with the manga in the .csv file
    db = Database(databasePath)
    # db.displayDatabase()
    # print("Database length : ", len(db.database) )

    website_url = "http://www.japscan.cc/mangas/"
    list_path = "list.csv"

    response = requests.get(website_url)
    # Get the data from the url in text format
    data = response.text
    soup = BeautifulSoup(data, 'lxml')

    # Search for <div id="liste_mangas">

    content = soup.find('div', {'id' : 'liste_mangas'})
    # If he doesn't find it -> quit the program
    if type(content) == 'NoneType':
        print("<div id=\"liste_mangas\"> was not found...")
        exit()
    # If he does fint it
    # print("Successfully Found")
    print("I'll check the following manga : ")
    for manga in db.database:
        # print("\t- ", manga)
        # Replace the spaces by an '-'
        manga_search = manga.replace(' ', '-')
        manga_search = manga_search.lower()
        manga_search = "/mangas/" + manga_search + "/"
        # print("Link :", manga_search)
        found = content.find('a', {'href' : manga_search} )
        # Check wether or not it found the manga we're looking for
        if ( found != None):
            # print("Found!")
            print("href : ", found['href'])
        else:
            print(manga + " not found")

    # for link in content.find_all('a', 'href' ):

