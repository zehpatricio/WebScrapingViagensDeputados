# WebScrapingViagensDeputados
Web Scraping dos dados das viagens oficiais dos deputados federais brasileiros

## Preparação do Ambiente
Você precisará ter instalado o Python 3.5. Após instalado e configurado instale os pacotes necessários para a execução do projeto contidos no arquivo `requirements.pip`. Ou se preferir utilize o comando `pip install -r requirements.pip` que instalará todos os pacotes.

## Execução
Você pode executar o programa utilizando o seguinte comando:
```
python3 app.py -di <data_inicial> -df <data_final>
```
Onde os parâmetros `data_inicial` e `data_final` estão no formato *dd/mm/aaaa* e representam o período no qual devem ser buscadas as viagens. A `data_final` não é obrigatória, e se omitida serão buscadas todas as viagens da `data_inicial` até a data atual.
