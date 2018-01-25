import requests, lxml, click, re, pymodm
from lxml import etree
from pymodm import connect
from datetime import datetime
from models import *

URL_ROOT = 'http://www.camara.leg.br'
URL_ORIGIN = URL_ROOT + '/missao-oficial/missao-pesquisa'
URL_MONGODB = 'mongodb+srv://patriciosousafilho:patricio@cluster0-0oxvy.mongodb.net/test'

def remove_espacos(texto):
	return re.sub('[\t|\n|\r]', '', texto)

def request_viagens(data_inicial, data_final):
	"""
	Função para requisitar a página que contém as viagens ocorridas em determinado período.
	
	Parâmetros:
	data_inicial -- String no formato 'dd/mm/YYYY' representando o início do período a ser buscado
	data_final -- String no formato 'dd/mm/YYYY' representando o fim do período a ser buscado
	"""
	params = {'deputado':1, 'nome-deputado':'', 'nome-servidor':'',
				'nome-evento':'', 'dati':data_inicial, 'datf':data_final}
	response = requests.get(URL_ORIGIN, params=params)
	return response

def get_detalhes(detalhes_link):
	"""
	Função para requisitar, processar e retornar os detalhes de uma viagem com base no link para eles.
	
	Parâmetros:
	detalhes_link -- String contendo o link relativo da página dos detalhes da viagem requerida
	"""
	response = requests.get(URL_ROOT+detalhes_link)
	html = etree.HTML(response.text)
	lis = html.xpath('//div[@class="sessionBox gradient"]/ul/li')
	relatorio_link = html.xpath('//div[@class="listaAcoes leftPositioned"]/a')[0].attrib['href']
	
	detalhes = Detalhes()
	detalhes.quantidade_diarias = remove_espacos(lis[2].text.split(":")[1]).replace(",",".")
	detalhes.valor_diaria = remove_espacos(lis[3].text.split(":")[1]).replace(",",".")
	detalhes.tipo_passagem = remove_espacos(lis[4].text.split(":")[1])
	detalhes.relatorio_link = URL_ROOT+'/missao-oficial/'+relatorio_link
	return detalhes

def get_viagens_from_request(response):
	"""
	Função para processar e salvar as viagens com base na página HTML que as contêm.
	
	Parâmetros:
	response -- Resposta da requisição da página contendo as viagens a serem processadas e salvas
	"""
	viagens = []
	html = etree.HTML(response.text)
	linhas = html.xpath('//tbody[@class="coresAlternadas"]/tr')

	for linha in linhas:
		colunas = linha.getchildren()
		subcolunas = colunas[4].getchildren()[0].getchildren()[0].getchildren()
		situacao = remove_espacos(subcolunas[1].text)
		detalhes = None
		if situacao == '':
			situacao = 'Disponível'
			detalhes_link = subcolunas[1].getchildren()[0].attrib['href']
			detalhes_link = remove_espacos(detalhes_link)
			detalhes = get_detalhes(detalhes_link)
		
		viagem = Viagem()
		viagem.inicio = datetime.strptime(colunas[0].text, '%Y-%m-%d')
		viagem.termino = datetime.strptime(colunas[1].text, '%Y-%m-%d')
		viagem.assunto = colunas[2].text
		viagem.destino = colunas[3].text
		viagem.deputado = subcolunas[0].getchildren()[0].text
		viagem.is_cancelada = (colunas[5].text == 'Sim')
		viagem.situacao = situacao
		if detalhes:
			viagem.detalhes = detalhes
		viagem.save()

		viagens.append(viagem)
	return viagens

@click.command()
@click.option('-di', '--datainicial', default=None, help='Data inicial das viagens a serem importados. É um parâmetro obrigatório. Formato dd/mm/aaaa.')
@click.option('-df', '--datafinal', default=None, help='Data final das viagens a serem importados. NÃO é um parâmetro obrigatório. Formato dd/mm/aaaa.')
def do_scraping(datainicial, datafinal):
	"""
	Essa função verifica os formatos de data e realiza a busca, processamento e persistência das viagens.
	
	Parâmetros:
	datainicial -- String no formato 'dd/mm/YYYY'
	datafinal -- String no formato 'dd/mm/YYYY'
	"""
	if datainicial:
		try:
			datetime.strptime(datainicial, '%d/%m/%Y')
			if not datafinal:
				datafinal = datetime.now().strftime('%d/%m/%Y')
			else:
				datetime.strptime(datafinal, '%d/%m/%Y')
			
			connect(URL_MONGODB)
			res = request_viagens(datainicial, datafinal)
			viagens = get_viagens_from_request(res)
			print(str(len(viagens))+' Viagens salvas com sucesso')
		except ValueError:
			print('Data em formato inválido')
			return 
	else:
		print('A data inicial é obrigatória')

if __name__ == '__main__':
	do_scraping()