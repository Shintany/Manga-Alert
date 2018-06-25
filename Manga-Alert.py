from bs4 import BeautifulSoup
import re
import string
import requests
from Classes.Test import Test
from Classes.tools import Database
from Classes.tools import Email
from Classes.PageCombiner import PageCombiner
import sys
import os

filename = "list.csv"
test = Test(filename)
test.run()

if __name__ == "__main__":
    # if len(sys.argv) != 2:
        # print ("Argument missing...")
        # print("Usage : python3 Manga-Alert.py $databasePath")
        # exit()
    databasePath = "list.csv"

    # Filling the dictionnary with the manga in the .csv file
    db = Database(databasePath)
    website_url = "http://www.japscan.cc/mangas/"
    list_path = "list.csv"

    new_manga = False

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
                    if not "." in last_chapter:
                        last_chapter = int(last_chapter.replace('/',''))

                        # Get the manga's last chapter in the database and then compare them
                        db_manga_last_chapter = int(db.database[manga])
                        if last_chapter > db_manga_last_chapter:
                            content_for_mail = manga + " : " + str(last_chapter - db_manga_last_chapter) + " chapters to read!\n"
                            mail.addContent(content_for_mail)

                            # List all the chapters' name
                            all_chapters = mangaPage_content.find_all('a', {'href' : re.compile(r".*")})
                            chapter_nb = last_chapter

                            # Looping over every manga's chapters
                            for chapter in all_chapters:
                                if chapter_nb > db_manga_last_chapter:
                                    
                                    ######################################
                                    # MAYBE HAVE TO PASS BY A TXT FILE...
                                    # Saving manga's title
                                    chapter_title_str = ""
                                    chapter_title_str += chapter.get_text()
                                    content_for_mail = ""
                                    if not ("Spoiler" in chapter_title_str):

                                        new_manga = True
                                        if (str(chapter_nb) in chapter_title_str):
                                            content_for_mail += "-> " + chapter_title_str + "\n"
                                            mail.addContent(content_for_mail) 
                                            p = PageCombiner(manga, chapter_nb, "https:" + chapter['href'])
                                            mail.addAttachments(p.out_filename)
                                            chapter_nb = chapter_nb - 1
                                    else:
                                        print(str(chapter_nb) + " is a spoiler...")
                                        chapter_nb = chapter_nb - 1
                                else:
                                    mail.addContent('\n\t\t------------------\n\n')
                                    break
                            db.database[manga] = last_chapter
                        # If the user entered a chapter number greater than the latest release chapter
                        elif last_chapter < db_manga_last_chapter:
                            content_for_mail = " - " + manga + " : The chapter number you entered in the database is greater than the latest released chapter...\n\n"
                            mail.addContent(content_for_mail)
                            db.database[manga] = last_chapter
                        else:
                            content_for_mail = manga + " : You're already up to date\n\n"
                            mail.addContent(content_for_mail)
                else:
                    print("manga_content didn't find : <div id=\"liste_chapitres\">")
            else:
                print("Manga url didn't respond")
        else:
            print(manga + " not found")
    
    # Sending mail to the user
    if new_manga == True:
        # mail.displayMailContent()
        mail.sendMail()
        db.updateDatabase()
        print("New release!")
        mail.deleteAttachments()
    else:
        print("No release...")



