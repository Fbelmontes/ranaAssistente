import requests
from bs4 import BeautifulSoup
import streamlit as st

def buscar_informacoes(termo):
    """
    Função para buscar informações sobre um link de site ou nome de empresa.
    """
    dados = {}
    
    if termo.startswith("http://") or termo.startswith("https://"):
        dados["tipo"] = "site"
        dados["url"] = termo
        try:
            # Web scraping básico
            response = requests.get(termo)
            soup = BeautifulSoup(response.text, "html.parser")
            
            # Pegando título da página
            dados["titulo"] = soup.title.string if soup.title else "Sem título"
            
            # Pegando meta descrição
            dados["descricao"] = soup.find("meta", attrs={"name": "description"})["content"] if soup.find("meta", attrs={"name": "description"}) else "Sem descrição"
            
            # Pegando o primeiro link de contato
            dados["contato"] = soup.find("a", href=True).text if soup.find("a", href=True) else "Sem contato encontrado"
        except Exception as e:
            dados["erro"] = f"Erro ao acessar o site: {e}"
    else:
        dados["tipo"] = "empresa"
        dados["nome"] = termo
        dados["informacoes"] = f"Informações sobre {termo} ainda não estão disponíveis diretamente."
    
    return dados
