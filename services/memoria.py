import json
from services.google_sheets import conectar_sheets
from services.google_sheets import conectar_arquivo_sheets



def recuperar_aprendizado(termo):
    sheet = conectar_sheets()
    try:
        aba = sheet.worksheet("Memoria")
        registros = aba.get_all_records()
        for r in registros:
            if r["Termo"].lower() == termo.lower():
                return json.loads(r["Contexto"])
    except:
        pass
    return None

def salvar_aprendizado(titulo, conteudo):
    sheet = conectar_sheets()

    try:
        aba = sheet.worksheet("Memoria")
    except:
        aba = sheet.add_worksheet(title="Memoria", rows="1000", cols="2")
        aba.append_row(["titulo", "conteudo"])

    aba.append_row([titulo, conteudo])

def ler_toda_memoria():
    sheet = conectar_sheets()
    try:
        aba = sheet.worksheet("Memoria")
    except:
        return []

    linhas = aba.get_all_records()
    return [f"Título: {linha['titulo']}\nConteúdo: {linha['conteudo']}" for linha in linhas]