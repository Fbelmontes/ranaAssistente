import gspread
import datetime
import json
import streamlit as st
from oauth2client.service_account import ServiceAccountCredentials
from config import SPREADSHEET_URL, CREDENTIALS_PATH

def conectar_sheets():
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    cred_dict = json.loads(st.secrets["GOOGLE_SHEETS_CREDENTIALS"])
    creds = ServiceAccountCredentials.from_json_keyfile_dict(cred_dict, scope)
    client = gspread.authorize(creds)
    return client.open_by_url(SPREADSHEET_URL).sheet1

def obter_conteudo_salvo():
    sheet = conectar_sheets()
    return sheet.get_all_records()

def salvar_transcricao(conteudo):
    sheet = conectar_sheets()
    sheet.append_row(["Reunião", conteudo])
    
def salvar_na_planilha(url, conteudo):
    sheet = conectar_sheets()
    sheet.append_row([url, conteudo])

def salvar_na_memoria(conteudo, nome_arquivo="Desconhecido"):
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name(CREDENTIALS_PATH, scope)
    client = gspread.authorize(creds)
    planilha = client.open_by_url(SPREADSHEET_URL)

    try:
        aba = planilha.worksheet("Base")
    except gspread.exceptions.WorksheetNotFound:
        aba = planilha.add_worksheet(title="Base", rows="1000", cols="2")
        aba.append_row(["URL", "Conteudo"])

    aba.append_row([nome_arquivo, conteudo])
    return True

def buscar_na_memoria(palavra_chave):
    sheet = conectar_sheets()
    dados = sheet.get_all_records()  # Pega todas as linhas da planilha

    resultados = []
    for registro in dados:
        nome_arquivo = registro.get("URL", "")
        conteudo = registro.get("Conteudo", "")
        
        # Verifica se a palavra chave está presente no conteúdo (ignorando maiúsculas/minúsculas)
        if palavra_chave.lower() in conteudo.lower():  
            resultados.append({"Nome do Arquivo": nome_arquivo, "Conteudo": conteudo})

    return resultados

def salvar_historico(pergunta, resposta):

    sheet = conectar_sheets()
    try:
        aba = sheet.spreadsheet.worksheet("Histórico")
    except:
        aba = sheet.spreadsheet.add_worksheet(title="Histórico", rows="1000", cols="3")
        aba.append_row(["Data/Hora", "Pergunta", "Resposta"])

    data_hora = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    aba.append_row([data_hora, pergunta, resposta])

def obter_historico(limit=5):
    sheet = conectar_sheets()
    aba = sheet.spreadsheet.worksheet("Histórico")
    dados = aba.get_all_records()
    return dados[-limit:]   

def obter_ultimas_interacoes(qtd=3):
    sheet = conectar_sheets()
    try:
        aba = sheet.spreadsheet.worksheet("Histórico")
        dados = aba.get_all_records()
        return dados[-qtd:]
    except:
        return []

def obter_conteudo_salvo():
    # Lê as credenciais do Google Sheets armazenadas no Streamlit Secrets
    creds_info = json.loads(st.secrets["GOOGLE_SHEETS_CREDENTIALS"])
    creds = Credentials.from_service_account_info(
        creds_info,
        scopes=["https://www.googleapis.com/auth/spreadsheets"]
    )
    
    # Cria o serviço da API Google Sheets
    service = build('sheets', 'v4', credentials=creds)

    # URL completa da planilha
    SPREADSHEET_URL = "https://docs.google.com/spreadsheets/d/1YnX5Lg7eW6AXwSdo73SIwvlxc4fITwUw5mTPHlspSqA/edit"
    
    # Extrair o ID da planilha da URL
    SPREADSHEET_ID = re.search(r'/d/([a-zA-Z0-9-_]+)', SPREADSHEET_URL).group(1)

    # Defina o intervalo de dados a ser lido
    range_ = "WebSubmit!A1:F"  # O nome da aba com dados do Web Summit

    # Chama a API para acessar os dados da planilha
    result = service.spreadsheets().values().get(spreadsheetId=SPREADSHEET_ID, range=range_).execute()
    values = result.get('values', [])

    if not values:
        print("Nenhum dado encontrado.")
        return []

    dados = []
    # Processa os dados da planilha
    for row in values:
        dados.append({
            "Título": row[0],
            "Horário": row[1],
            "Local": row[2],
            "Tag": row[3],
            "Descrição": row[5],  # Correção de índice, coluna 5 para Descrição
            "Palestrantes": row[6]  # Correção de índice, coluna 6 para Palestrantes
        })
    
    return dados