import requests
from services.google_sheets import conectar_sheets
from services.hubspot_oauth import renovar_token_automaticamente
from collections import defaultdict

PLANILHA_ID = "1YnX5Lg7eW6AXwSdo73SIwvlxc4fITwUw5mTPHlspSqA"
ABA_VERIFICAR = "Verificar_Leads"

# Define pesos para cada campo usado na comparação
PESOS = {
    "firstname": 2,
    "lastname": 2,
    "company": 3,
    "linkedin": 3,
    "jobtitle": 1
}

def buscar_leads_na_base():
    access_token = renovar_token_automaticamente()
    aba = conectar_sheets().worksheet(ABA_VERIFICAR)
    dados = aba.get_all_records()

    for i, linha in enumerate(dados):
        nome = linha.get("Nome", "").strip()
        sobrenome = linha.get("Sobrenome", "").strip()
        empresa = linha.get("Empresa", "").strip()
        linkedin = linha.get("Linkedin", "").strip()
        cargo = linha.get("Cargo", "").strip()

        filtros = []
        if nome:
            filtros.append({"propertyName": "firstname", "operator": "CONTAINS_TOKEN", "value": nome})
        if sobrenome:
            filtros.append({"propertyName": "lastname", "operator": "CONTAINS_TOKEN", "value": sobrenome})
        if empresa:
            filtros.append({"propertyName": "company", "operator": "CONTAINS_TOKEN", "value": empresa})
        if linkedin:
            filtros.append({"propertyName": "linkedin", "operator": "CONTAINS_TOKEN", "value": linkedin})
        if cargo:
            filtros.append({"propertyName": "jobtitle", "operator": "CONTAINS_TOKEN", "value": cargo})

        payload = {
            "filterGroups": [{"filters": filtros}],
            "properties": ["firstname", "lastname", "company", "email", "jobtitle", "linkedin"],
            "limit": 10
        }

        url = "https://api.hubapi.com/crm/v3/objects/contacts/search"
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }

        res = requests.post(url, headers=headers, json=payload)

        if res.status_code != 200:
            aba.update_cell(i+2, 7, "Erro na API")
            aba.update_cell(i+2, 10, res.text)
            continue

        resultados = res.json().get("results", [])
        if not resultados:
            aba.update_cell(i+2, 7, "Novo lead")
            aba.update_cell(i+2, 10, "Nenhum contato encontrado")
            continue

        # Avaliar todos os resultados e atribuir scores
        scores = []
        for contato in resultados:
            props = contato.get("properties", {})
            score = 0
            for campo in ["firstname", "lastname", "company", "linkedin", "jobtitle"]:
                valor = linha.get(campo.capitalize(), "").strip().lower()
                if valor and valor in props.get(campo, "").lower():
                    score += PESOS[campo]
            scores.append({"score": score, "id": contato.get("id"), "email": props.get("email"), "company": props.get("company"), "nome": props.get("firstname"), "sobrenome": props.get("lastname")})

        # Ordenar pelo score
        scores.sort(key=lambda x: x["score"], reverse=True)
        melhor = scores[0] if scores else {}

        status = "Match exato" if melhor.get("score", 0) >= 6 else "Possível match"

        aba.update_cell(i+2, 7, status)
        aba.update_cell(i+2, 8, melhor.get("id", ""))
        aba.update_cell(i+2, 9, melhor.get("email", ""))
        aba.update_cell(i+2, 10, f"Empresa: {melhor.get('company', '')} | Nome: {melhor.get('nome', '')} {melhor.get('sobrenome', '')}")
