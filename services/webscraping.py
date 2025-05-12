import requests
from bs4 import BeautifulSoup
import streamlit as st

def buscar_informacoes(termo):
    """
    Função para buscar informações sobre uma empresa usando a Hunter.io API.
    """
    dados = {}
    dominio = termo.split("://")[1] if "://" in termo else termo

    # Configuração da chave da API Hunter.io
    api_key = st.secrets["HUNTER_API"] # Substitua com sua chave da API do Hunter.io
    api_url = f"https://api.hunter.io/v2/domain-search?domain={dominio}&api_key={api_key}"

    try:
        response = requests.get(api_url)
        if response.status_code == 200:
            empresa_data = response.json()
            dados["nome"] = empresa_data.get("data", {}).get("organization", "Nome não encontrado")
            dados["setor"] = empresa_data.get("data", {}).get("industry", "Setor não encontrado")
            dados["funcionarios"] = empresa_data.get("data", {}).get("employees", "Número de funcionários não encontrado")
            dados["tamanho"] = empresa_data.get("data", {}).get("size", "Tamanho não encontrado")
            dados["localizacao"] = empresa_data.get("data", {}).get("location", "Localização não encontrada")
            dados["descricao"] = empresa_data.get("data", {}).get("description", "Descrição não disponível")
        else:
            dados["erro"] = "Erro ao acessar dados da empresa."
    except Exception as e:
        dados["erro"] = f"Erro na chamada à API: {e}"

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

    