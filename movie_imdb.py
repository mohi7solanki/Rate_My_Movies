try:
    import sys
    import requests
    import subprocess
    import os
    from bs4 import BeautifulSoup
    from pyfiglet import Figlet
except:
    print('Please install reqeusts, pyfiglet and bs4 module')
    sys.exit(1)

search_url = 'http://www.google.co.in/search?q={}+ imdb'

f = Figlet(font='big')
print(f.renderText('Rate My Movies'))
f = Figlet(font='speed')
print(f.renderText('by\nMohit'))

try:
    movie_list = os.listdir(input('Please Enter path to Movie directory: '))
except:
    print('Please Enter a valid path')
    sys.exit(1)

sorted_movie = set()

def get_movie_page(movie_name):
    page = requests.get(search_url.format(movie_name))
    return page.text


def get_imdb_link(html_page):
    soup = BeautifulSoup(html_page,'html.parser')
    link = soup.findAll('cite')[0].text
    return link

def get_imdb_rating(imdb_page):
    page = requests.get('http://'+imdb_page)
    soup = BeautifulSoup(page.text,'html.parser')
    rating = soup.findAll('div',{'class':'ratingValue'})[0].text.strip().split('/')[0]
    name = soup.title.text.split('-')[0].strip()
    return name, rating

subprocess.Popen(['notify-send',';) Sit Back and relax While I help you decide Which Movie to watch :)'])


for movie in movie_list:
    try:
        movie_page = get_movie_page(movie)
        imdb_link = get_imdb_link(movie_page)
        movie_name, rating = get_imdb_rating(imdb_link)
        sorted_movie.add((movie_name, rating))
    except:
        if len(movie) >= 30:
            try:
                movie_page = get_movie_page(movie[:30])
                imdb_link = get_imdb_link(movie_page)
                movie_name, rating = get_imdb_rating(imdb_link)
                sorted_movie.add((movie_name, rating))
            except:
                print("Couldn't fetch details for this movie: "+movie)

sorted_movie = sorted(sorted_movie, key=lambda x: x[1], reverse = True)


with open('rateMyMovie.txt','w') as file:
    for movie in sorted_movie:
        file.write('{} {}\n'.format(movie[0].ljust(40), movie[1]))

for movie in sorted_movie:
    print('\n{} {}'.format(movie[0].ljust(40), movie[1]))



subprocess.Popen(['notify-send',';) Work Done'])
