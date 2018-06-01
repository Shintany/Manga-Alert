from bs4 import BeautifulSoup
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
    print(databasePath)

    # Filling the dictionnary with the manga in the .csv file
    db = Database(databasePath)
    print(db.database.get("One piece"))
    print(db.database.get("My Hero Academia"))

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
    else:
        print("Successfully Found")
        # for link in content.find_all('a', 'href' ):

