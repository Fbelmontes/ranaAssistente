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

def salvar_historico(pergunta, resposta):

    sheet = conectar_sheets()
    try:
        aba = sheet.spreadsheet.worksheet("Historico")
    except:
        aba = sheet.spreadsheet.add_worksheet(title="Historico", rows="1000", cols="3")
        aba.append_row(["Data/Hora", "Pergunta", "Resposta"])

    data_hora = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    aba.append_row([data_hora, pergunta, resposta])

    # Função para salvar informações na Google Sheets

def salvar_na_planilha_2(termo, dados):
    """
    Função para salvar informações sobre uma empresa ou site na planilha Google Sheets.
    :param termo: o nome da empresa ou link do site
    :param dados: os dados coletados relacionados ao termo
    """
    sheet = conectar_sheets()

    # Verificar se as colunas já existem, caso contrário, criar novas
    try:
        aba = sheet.worksheet("Base")
    except gspread.exceptions.WorksheetNotFound:
        aba = sheet.add_worksheet(title="Base", rows="1000", cols="2")
        aba.append_row(["Termo", "Dados"])

    # Corrigir a codificação para garantir que caracteres especiais sejam salvos corretamente
    termo = termo.strip().encode('utf-8').decode('utf-8')  # Garantir que o termo esteja corretamente codificado
    dados = json.dumps(dados, ensure_ascii=False)  # Garantir que os dados sejam salvos corretamente com UTF-8

    # Salvar as informações coletadas
    aba.append_row([termo, dados])

    st.success("Informações salvas com sucesso!")
    return True
