import gspread
import datetime
from oauth2client.service_account import ServiceAccountCredentials
from config import SPREADSHEET_URL, CREDENTIALS_PATH

def conectar_sheets():
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name(CREDENTIALS_PATH, scope)
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
