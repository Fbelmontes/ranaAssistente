import json
from services.google_sheets import conectar_sheets, conectar_arquivo_sheets 


def salvar_aprendizado(termo, contexto):
    sheet = conectar_sheets()
    try:
        aba = sheet.worksheet("Memoria")
    except:
        aba = sheet.add_worksheet(title="Memoria", rows="1000", cols="2")
        aba.append_row(["Termo", "Contexto"])

    aba.append_row([termo, json.dumps(contexto, ensure_ascii=False)])

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

def ler_toda_memoria():
    sheet = conectar_arquivo_sheets()
    try:
        aba = sheet.worksheet("Memoria")
        registros = aba.get_all_records()
        memoria = {r["Termo"]: json.loads(r["Contexto"]) for r in registros}
        return memoria
    except:
        return {}