from bs4 import BeautifulSoup
import requests

class Menu():
    def __init__(self, url=""):

        self.url = url

        # Get Manga List
        self.manga_list = self.getMangaName()

        print('There\'s ' + str(len(self.manga_list)) + ' mangas')

    def getMangaName(self):

        print('Getting manga list')

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

        manga_list = []

        print('Going into the loop')
        for manga in manga_list_content.find_all('a'):
            if '/mangas/' in manga['href']:
                manga_name = manga['href'].replace('/mangas/', '')
                manga_name = manga_name.replace('/', '')
                # print('Manga : ' + manga_name)
                manga_list.append(manga_name)
        
        return manga_list

