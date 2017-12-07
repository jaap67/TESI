import requests
import time

from bs4 import BeautifulSoup

link_base = "http://example.webscraping.com"
link_page = link_base + "/places/default/index/"

def run(link):
    if link is None:
        return

    for i in range(0,25):
        if i == 0:
            soup = get_html(link)
        else:
            url = link_page + str(i)
            soup = get_html(url)

        if soup is None:
            return

        result = soup.find(attrs={'id': 'results'})

        for texto in result.find_all('a'):
            link = texto.get('href')
            get_data_child(link_base + link)
            time.sleep(1)

def get_data_child(link):

    soup = get_html(link)

    if soup is None:
        return

    tr = soup.find(attrs={'id': 'places_country__row'})
    country = tr.find(attrs={'class': 'w2p_fw'}).text
    tr = soup.find(attrs={'id': 'places_area__row'})
    area = tr.find(attrs={'class': 'w2p_fw'}).text
    area = area.split()[0].replace(',', '')
    tr = soup.find(attrs={'id': 'places_population__row'})
    population = tr.find(attrs={'class': 'w2p_fw'}).text
    population = population.replace(',', '')
    densidade = '{:,.2f}'.format(float(population) / float(area))

    print("======================================")
    print(country)
    print(area)
    print(population)
    print(densidade)
    print("======================================")

def get_html(link):
    response = requests.get(link)
    return BeautifulSoup(response.text, 'html5lib')

if __name__ == "__main__":
    run(link_base + '/places')