from bs4 import BeautifulSoup
from urllib.request import urlopen

link_base = 'file:///Users/macuser/TESI/tesi02/rotten.html'

def run(link):

    if link is None:
        return

    soup = get_html(link)

    if soup is None:
        return

    result = soup.find_all('div', class_='movie_info')

    for movie in result:
        titulo = movie.h3.text
        avaliacao = movie.span.text
        if avaliacao == '':
            avaliacao = 'n/a'

        print('{} - {}'.format(titulo, avaliacao))

def get_html(link):
    parser = 'html.parser'
    markup = urlopen(link).read()
    return BeautifulSoup(markup, parser)

if __name__ == "__main__":
    run(link_base)