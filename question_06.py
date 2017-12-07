import requests
from bs4 import BeautifulSoup
from money import Money
import csv

link_base = 'http://www.portaltransparencia.gov.br/copa2014/api/rest/empreendimento'
link_base_local = 'file:///Users/macuser/TESI/tesi02/empreendimento.xml'

def run(link):

    if link is None:
        return

    soup = get_html(link)

    if soup is None:
        return

    empreendimentos = soup.find_all('copa:empreendimento')

    sedes = []
    ids = []

    for empreendimento in empreendimentos:

        if empreendimento.ativo.text == 'true':

            id = int(empreendimento.cidadeSede.id.text)
            sede = empreendimento.cidadeSede.descricao.text

            try:
                valor_previsto = float(empreendimento.valorTotalPrevisto.text)
            except AttributeError:
                valor_previsto = 0
            try:
                valor_executado = float(empreendimento.valorPercentualExecucaoFisica.text) * valor_previsto / 100
            except AttributeError:
                valor_executado = 0

            sedes.append({'id': id, 'sede': sede, 'valor_previsto': valor_previsto, 'valor_executado': valor_executado})

        if id not in ids:
            ids.append(id)

    ids.sort()
    resultados = []

    for id in ids:
        total_previsto_sede = 0
        total_gasto_sede = 0
        resultado_sede = {}

        for sede in sedes:

            if id == sede['id']:
                total_previsto_sede += sede['valor_previsto']
                total_gasto_sede += sede['valor_executado']
                resultado_sede = {'id': id, 'sede': sede['sede'], 'total_previsto': total_previsto_sede, 'total_gasto': total_gasto_sede}

        resultados.append(resultado_sede)

    with open('empreendimentos.csv', 'w', newline='') as csvfile:
        fieldnames = ['id', 'sede', 'total_previsto', 'total_gasto']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(resultados)


    for resultado in resultados:
        print('Id {}'.format(resultado['id']))
        print('Sede {}'.format(resultado['sede']))
        print('Total Previsto {}'.format(Money(resultado['total_previsto'], 'BRL').format('pt_BR')))
        print('Total Gasto {}'.format(Money(resultado['total_gasto'], 'BRL').format('pt_BR')))

def get_html(link):
    response = requests.get(link)
    return BeautifulSoup(response.text, 'xml')

if __name__ == "__main__":
    run(link_base)