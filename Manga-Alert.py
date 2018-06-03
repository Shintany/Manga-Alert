from bs4 import BeautifulSoup
import string
import requests
from test import Test
from tools import Database
from tools import Email
import sys

filename = "list.csv"
test = Test(filename)
test.run()

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print ("Argument missing...")
        print("Usage : python3 Manga-Alert.py $databasePath")
        exit()
    databasePath = sys.argv[1]

    # Filling the dictionnary with the manga in the .csv file
    db = Database(databasePath)
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
    # Preparing the Email object
    mail = Email()

    for manga in db.database:
        # Replace the spaces by an '-'
        manga_search = manga.replace(' ', '-')
        manga_search = manga_search.lower()

        # Saving the manga name avec '-' instead of spaces
        manga_lower = manga_search
        manga_search = "/mangas/" + manga_search + "/"
        found = content.find('a', {'href' : manga_search} )

        # Check whether or not it found the manga we're looking for
        if ( found != None):
            manga_search_url = "http://www.japscan.cc" + manga_search
            manga_response = requests.get(manga_search_url)
            if manga_response.status_code == 200:
                mangaPage_data = manga_response.text
                mangaPage_soup = BeautifulSoup(mangaPage_data, 'lxml')

                # Search for <div id="liste_chapitres">
                mangaPage_content = mangaPage_soup.find('div', {'id' : 'liste_chapitres'})

                # If he found it
                if type(mangaPage_content) != 'NoneType':
                    last_chapter_url = mangaPage_content.find('a')

                    # Setting the string to remove in order to get the chapter number
                    str_to_remove = "//www.japscan.cc/lecture-en-ligne/" + manga_lower + "/"
                    last_chapter = last_chapter_url['href'].replace(str_to_remove, '')
                    last_chapter = int(last_chapter.replace('/',''))

                    # Get the manga's last chapter in the database and then compare them
                    db_manga_last_chapter = int(db.database[manga])
                    if last_chapter > db_manga_last_chapter:
                        content_for_mail = " - " + manga + " : " + str(last_chapter - db_manga_last_chapter) + " chapters to read!\n\n"
                        mail.addContent(content_for_mail)
                        db.database[manga] = last_chapter
                else:
                    print("manga_content didn't find : <div id=\"liste_chapitres\">")
            else:
                print("Manga url didn't respond")
        else:
            print(manga + " not found")
    
    # Sending mail to the user
    mail.sendMail()
    db.updateDatabase()



