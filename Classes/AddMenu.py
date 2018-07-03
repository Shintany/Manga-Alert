from bs4 import BeautifulSoup
import requests

class Menu():
    def __init__(self, url=""):

        self.url = url

        # Get Manga List
        self.manga_list = self.getMangaName()

        continue_to_add = True

        while continue_to_add:
            # Get the Manga name fron the user
            self.addManga()

            # Ask whether the user want to add another manga
            choice = input('Add another manga? (Y/n) : ')
            if choice == 'N' or choice == 'n':
                continue_to_add = False


    def getMangaName(self):

        # Initializing void dictionnary
        manga_list = []
        manga_list_response = requests.get(self.url)
        
        # Get the data from the url in text format
        manga_list_data = manga_list_response.text
        manga_list_soup = BeautifulSoup(manga_list_data, 'lxml')

        # Search for <div id="list_mangas">
        manga_list_content = manga_list_soup.find('div', {'id' : 'liste_mangas'})

        # If he doesn't find it -> quit the program
        if type(manga_list_content) == 'NoneType':
            print("<div id=\"liste_mangas\"> was not found...")
            exit()

        # Getting all manga name and put them in a dictionnary
        for manga in manga_list_content.find_all('a'):
            if '/mangas/' in manga['href']:
                manga_name = manga['href'].replace('/mangas/', '')
                manga_name = manga_name.replace('/', '')
                manga_list.append(manga_name)
        
        return manga_list

    def addManga(self):

        # Getting manga name and chapter
        manga_name = input('Enter the manga name : ')
        last_chapter_read = int(input('The last chapter number you\'ve read : '))

        # Creating string to add in the .csv file
        adding_line = manga_name + ',' + str(last_chapter_read) + '\n'

        try:
            # Append the line into .csv file
            with open('list.csv', 'a') as db:
                db.write(adding_line)
        except:
            print('Error when writing in the .csv file')
            exit()
        
        print('Line added succesfully!')


