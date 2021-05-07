from nltk.corpus import stopwords
import nltk
from bs4 import BeautifulSoup
import requests
import os

def removeStopwords_1():
    ''' Nesta função as palavras de apoio da língua portugesa são agrupadas em forma de lista para
    formar as chamadas "Stopwords", utilizando a lib nltk.'''
    
    stopwords_lista = stopwords.words('portuguese')
    return stopwords_lista
        
def listaVerbos():
    ''' Nesta função são agrupados os verbos da língua portugesa, disponíveis no site "Conjugação.com.br"'''
    verbos = []
    for pagina in range(1,51):
        site = requests.get(f'https://www.conjugacao.com.br/verbos-populares/{pagina}/').content
        soup = BeautifulSoup(site)
        lista = soup.find_all('li')

        for a in lista:
            verbos.append(str(a).split('a href')[1].split('title')[0].split('/')[1].replace('verbo-',''))
    return verbos

def retornaListaSwCompleta():
    ''' Esta função agrega a lista de Stopwords gerada pela lib NLTK com a lista de verbos da 
    língua portugesa.'''
    stopwords = removeStopwords_1()
    verbos = listaVerbos()
    stopwords_final = stopwords + verbos
    with open(os.path.join(os.getcwd(),'config','lista_stopwords.txt'), 'w') as f:
        s1='\n'.join(stopwords_final)
        f.write(s1)
        f.close()

print("Executando ...")
retornaListaSwCompleta()
print("Finished")
