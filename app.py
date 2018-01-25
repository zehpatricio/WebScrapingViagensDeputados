import requests, lxml, click, re
from lxml import etree
from datetime import datetime

URL_ORIGIN='http://www.camara.leg.br/missao-oficial/missao-pesquisa'

def request_viagens(data_inicial, data_final):
	dati = '{}/{}/{}'.format(data_inicial.day, data_inicial.month, data_inicial.year)
	datf = '{}/{}/{}'.format(data_final.day, data_final.month, data_final.year)
	params = {'deputado':1, 'nome-deputado':'', 'nome-servidor':'', 
				'nome-evento':'', 'dati':dati, 'datf':datf}
	response = requests.get(URL_ORIGIN, params=params)
	return response

def get_viagens_from_request(response):
	viagens = []
	html = etree.HTML(response.text)
	linhas = html.xpath('//tbody[@class="coresAlternadas"]/tr')

	for linha in linhas:
		colunas = linha.getchildren()
		subcolunas = colunas[4].getchildren()[0].getchildren()[0].getchildren()
		situacao = re.sub('[\t|\n|\r| ]', '', subcolunas[1].text.lower())
		deputado = subcolunas[0].getchildren()[0].text
		
		viagem = {'inicio':colunas[0].text, 'termino':colunas[1].text, 
					'assunto':colunas[2].text, 'destino': colunas[3].text,
					'deputado':deputato, 'cancelada': colunas[5].text, 
					'situacao': situacao}
		viagens.append(viagens)
	return viagens