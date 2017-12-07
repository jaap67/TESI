import requests
from bs4 import BeautifulSoup
from money import Money

link_base = 'http://www.portaltransparencia.gov.br/copa2014/api/rest/empreendimento'

def run(link):

    if link is None:
        return

    soup = get_html(link)

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

    print('Total previsto: {}  -  Total gasto: {}'.format(Money(total_previsto, 'BRL').format('pt_BR'), Money(total_gasto, 'BRL').format('pt_BR')))

def get_html(link):
    response = requests.get(link)
    return BeautifulSoup(response.text, 'xml')

if __name__ == "__main__":
    run(link_base)