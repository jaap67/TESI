import requests
import csv

from bs4 import BeautifulSoup

link_base = 'http://www.imdb.com/chart/boxoffice'

def run(link):

    if link is None:
        return

    soup = get_html(link)

    if soup is None:
        return

    result = soup.find('tbody')
    title = result.find_all('td', class_='titleColumn')
    weekend = result.find_all('td', class_='ratingColumn')
    gross = result.find_all('span', class_='secondaryInfo')
    weeks = result.find_all('td', class_='weeksColumn')

    with open('topbox.csv', 'w') as csvfile:
        fieldnames = ['title', 'weekend', 'gross', 'weeks']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for i in range(len(title)):
            movie = {
                'title': title[i].a.text.strip(),
                'weekend': weekend[i].text.strip(),
                'gross': gross[i].text.strip(),
                'weeks': weeks[i].text.strip(),
            }
            writer.writerow(movie)


def get_html(link):
    response = requests.get(link)
    return BeautifulSoup(response.text, 'html5lib')

if __name__ == "__main__":
    run(link_base)