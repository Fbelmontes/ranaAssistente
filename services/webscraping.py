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

def buscar_dados_multiplas_paginas(url_base):
    """
    Função para buscar informações de um evento que está distribuído por várias páginas.
    """
    dados_completos = []  # Lista para armazenar todos os dados coletados
    
    pagina_atual = 1
    while True:
        # Constrói a URL da página atual
        url = f"{url_base}?page={pagina_atual}"
        
        try:
            # Faz a requisição para a página
            response = requests.get(url)
            soup = BeautifulSoup(response.text, "html.parser")
            
            # Extração dos dados da página (adaptar conforme sua estrutura)
            # Exemplo: pegando os nomes e URLs de cada perfil de participantes do evento
            participantes = soup.find_all(class_="ZwZBMLuwwYKLtqOdlRcByADgXVbjtIKaeTA")
            
            for participante in participantes:
                nome = participante.get_text()
                url_perfil = participante.find_parent("a")["href"]
                dados_completos.append({
                    "nome_linkedin": nome,
                    "url_linkedin": url_perfil
                })
            
            # Verifica se há uma próxima página (dependendo da estrutura, você pode procurar por um botão ou link de "próxima página")
            proxima_pagina = soup.find("a", text="Próxima")  # Adapte conforme o link de navegação da página
            if not proxima_pagina:
                break  # Se não houver próxima página, sai do loop
            
            pagina_atual += 1  # Caso haja próxima página, incrementa o contador
        
        except Exception as e:
            st.error(f"Erro ao acessar a página {pagina_atual}: {e}")
            break  # Interrompe caso haja erro
    
    return dados_completos

def scraping_evento_component():
    st.title("Web Scraping de Evento com Múltiplas Páginas")
    
    # Solicitar ao usuário a URL base do evento
    url_input = st.text_input("Insira a URL do evento (com paginação):")
    
    if url_input:
        # Chama a função de scraping
        dados = buscar_dados_multiplas_paginas(url_input)
        
        # Exibe os resultados ou erros
        if dados:
            st.success("Dados encontrados:")
            for dado in dados:
                st.write(f"Nome: {dado['nome_linkedin']}")
                st.write(f"URL do Perfil: {dado['url_linkedin']}")
        else:
            st.error("Nenhum dado encontrado ou erro ao acessar as páginas.")

    