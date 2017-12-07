import requests
from bs4 import BeautifulSoup
import mysql.connector

link_base = 'https://www.climatempo.com.br/previsao-do-tempo/cidade/264/teresina-pi'

def run(link):

    if link is None:
        return

    soup = get_html(link)

    if soup is None:
        return

    conn = connectDB()
    cursor = conn.cursor()

    insert = "INSERT INTO clima (localidade, temperatura, condicao, sensacao, humidade, pressao, vento, atualizacao) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"

    result = soup.find('div', class_='row top10')
    localidade = result.find('h1', {'id': 'momento-localidade'}).text
    temperatura = result.find('p', {'id': 'momento-temperatura'}).text
    condicao = result.find('p', {'id': 'momento-condicao'}).text
    sensacao = result.find('li', {'id': 'momento-sensacao'}).text
    humidade = result.find('li', {'id': 'momento-humidade'}).text
    pressao = result.find('li', {'id': 'momento-pressao'}).text
    vento = ''.join(result.find('a', {'id': 'momento-vento'}).text.split())
    atualizacao = result.find('p', {'id': 'momento-atualizacao'}).text.strip()

    dados = (localidade, temperatura, condicao, sensacao, humidade, pressao, vento, atualizacao)
    cursor.execute(insert, dados)
    conn.commit()
    cursor.close()
    conn.close()

    print('Locadidade {}'.format(localidade))
    print('Temperatura {}'.format(temperatura))
    print('Condição {}'.format(condicao))
    print('Sensação {}'.format(sensacao))
    print('Humidade {}'.format(humidade))
    print('Pressão {}'.format(pressao))
    print('Vento {}'.format(vento))
    print('Atualização {}'.format(atualizacao))

def connectDB():
    return mysql.connector.connect(user="root", password="root", host="localhost", database="weather", port="8889")

def get_html(link):
    response = requests.get(link)
    return BeautifulSoup(response.text, 'html5lib')

if __name__ == "__main__":
    run(link_base)