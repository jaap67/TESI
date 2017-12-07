from django.shortcuts import render, redirect
from questions.models import Question03
import requests
from bs4 import BeautifulSoup
from urllib.request import urlopen
import csv
import time
from money import Money

def get_html(link):
    response = requests.get(link)
    return BeautifulSoup(response.text, 'html5lib')

def get_html_urllib(link):
    parser = 'html.parser'
    markup = urlopen(link).read()
    return BeautifulSoup(markup, parser)

def get_html_xml(link):
    response = requests.get(link)
    return BeautifulSoup(response.text, 'xml')

def index(request):
    return render(request, 'index.html')

def question_01(request):
    
    link_base = 'file:///Users/macuser/TESI/tesi02/rotten.html'
    results = []
    
    if link_base is None:
        return

    soup = get_html_urllib(link_base)

    if soup is None:
        return

    result = soup.find_all('div', class_='movie_info')
    
    for movie in result:
        
        titulo = movie.h3.text
        print(titulo)
        avaliacao = movie.span.text
        print(avaliacao)
        if avaliacao == '':
            avaliacao = 'n/a'

        dadosDict = {'nome': titulo, 'avaliacao': avaliacao}
        results.append(dadosDict)
        
    return render(request, 'question_01.html', {'data': results})

def question_02(request):
    
    link_base = 'http://www.imdb.com/chart/boxoffice'
    
    if link_base is None:
        return

    soup = get_html(link_base)

    if soup is None:
        return

    result = soup.find('tbody')
    title = result.find_all('td', class_='titleColumn')
    weekend = result.find_all('td', class_='ratingColumn')
    gross = result.find_all('span', class_='secondaryInfo')
    weeks = result.find_all('td', class_='weeksColumn')
    
    results = []
    
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
            results.append(movie)
    
    return render(request, 'question_02.html', {'data': results})
    
    
def question_03(request):
    
    link_base = 'https://www.climatempo.com.br/previsao-do-tempo/cidade/264/teresina-pi'
    
    if link_base is None:
        return

    soup = get_html(link_base)

    if soup is None:
        return


    result = soup.find('div', class_='row top10')
    localidade = result.find('h1', {'id': 'momento-localidade'}).text
    temperatura = result.find('p', {'id': 'momento-temperatura'}).text
    condicao = result.find('p', {'id': 'momento-condicao'}).text
    sensacao = result.find('li', {'id': 'momento-sensacao'}).text
    humidade = result.find('li', {'id': 'momento-humidade'}).text
    pressao = result.find('li', {'id': 'momento-pressao'}).text
    vento = ''.join(result.find('a', {'id': 'momento-vento'}).text.split())
    atualizacao = result.find('p', {'id': 'momento-atualizacao'}).text.strip()
    
    if not Question03.objects.filter(atualizacao=atualizacao).exists():
        Question03.objects.create(localidade=localidade, temperatura=temperatura, condicao=condicao, sensacao=sensacao, humidade=humidade, pressao=pressao, vento=vento, atualizacao=atualizacao)
    
    data = Question03.objects.all()
    return render(request, 'question_03.html', {'data': data})
    
def question_04(request):

    link_base = "http://example.webscraping.com"
    link_page = link_base + "/places/default/index/"

    if link_base is None:
        return

    for i in range(0,25):
        if i == 0:
            soup = get_html(link_base)
        else:
            url = link_page + str(i)
            soup = get_html(url)

        if soup is None:
            return

        result = soup.find(attrs={'id': 'results'})
        
        result_list = []
        
        for texto in result.find_all('a'):
            link = texto.get('href')
            result_list.append(get_data_child(link_base + link))
            time.sleep(1)
            
    return render(request, 'question_04.html', {'data': result_list})
    


def get_data_child(link):
    
    dados_paginacao = {}
    
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
    
    dados_paginacao = {'country': country, 'area': area, 'population': population, 'densidade': densidade}
    return dados_paginacao

def question_05(request):
    
    link_base = 'http://www.portaltransparencia.gov.br/copa2014/api/rest/empreendimento'
    # link_base = 'file:///Users/macuser/TESI/tesi02/empreendimento.xml'

    if link_base is None:
        return

    soup = get_html_xml(link_base)

    if soup is None:
        return

    empreendimentos = soup.find_all('copa:empreendimento')
    total_previsto = 0
    total_gasto = 0
    
    for empreendimento in empreendimentos:
        if empreendimento.ativo.text == 'true':
            try:
                valor_previsto = float(empreendimento.valorTotalPrevisto.text)
            except AttributeError:
                valor_previsto = 0
            try:
                valor_executado = float(empreendimento.valorPercentualExecucaoFisica.text) * valor_previsto / 100
            except AttributeError:
                valor_executado = 0

            total_previsto += valor_previsto
            total_gasto += valor_executado
    
    data = {'total_previsto': str(total_previsto).format(Money(total_previsto, 'BRL').format('pt_BR')), 'total_gasto': str(total_gasto).format(Money(total_gasto, 'BRL').format('pt_BR'))}
    return render(request, 'question_05.html', {'data': data})

def question_06(request):
    pass