from bs4 import BeautifulSoup
import requests
verbos = []
for pagina in range(1,51):
    site = requests.get(f'https://www.conjugacao.com.br/verbos-populares/{pagina}/').content
    soup = BeautifulSoup(site)
    lista = soup.find_all('li')
    
    for a in lista:
        verbos.append(str(a).split('a href')[1].split('title')[0].split('/')[1].replace('verbo-',''))
    
