import requests
from bs4 import BeautifulSoup

def extrair_texto(url):
    try:
        resposta = requests.get(url)
        sopa = BeautifulSoup(resposta.text, 'html.parser')
        paragrafos = sopa.find_all('p')
        texto = ' '.join([p.get_text() for p in paragrafos])
        return texto.strip()
    except Exception as e:
        return f"Erro ao acessar o site: {e}"
