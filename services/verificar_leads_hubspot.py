import requests
from services.google_sheets import conectar_sheets
from services.hubspot_oauth import renovar_token_automaticamente

PLANILHA_ID = "1YnX5Lg7eW6AXwSdo73SIwvlxc4fITwUw5mTPHlspSqA"  # Memória da RANA
ABA_VERIFICAR = "Verificar_Leads"

def buscar_leads_na_base():
    access_token = renovar_token_automaticamente()
    aba = conectar_sheets(PLANILHA_ID).worksheet(ABA_VERIFICAR)
    dados = aba.get_all_records()
    
    for i, linha in enumerate(dados):
        nome = linha.get("Nome", "").strip()
        empresa = linha.get("Empresa", "").strip()
        email = linha.get("E-mail", "").strip()

        status = "Não encontrado"
        lead_id = ""
        lifecycle = ""
        obs = ""

        payload = {
            "filterGroups": [],
            "properties": ["email", "lifecyclestage", "company", "firstname", "lastname"],
            "limit": 3
        }

        if email:
            payload["filterGroups"].append({
                "filters": [{"propertyName": "email", "operator": "EQ", "value": email}]
            })
        else:
            filtros = []
            if nome:
                filtros.append({"propertyName": "firstname", "operator": "CONTAINS_TOKEN", "value": nome})
            if empresa:
                filtros.append({"propertyName": "company", "operator": "CONTAINS_TOKEN", "value": empresa})
            if filtros:
                payload["filterGroups"].append({"filters": filtros})

        url = "https://api.hubapi.com/crm/v3/objects/contacts/search"
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }

        res = requests.post(url, headers=headers, json=payload)

        if res.status_code == 200:
            resultado = res.json()
            resultados = resultado.get("results", [])
            if resultados:
                contato = resultados[0]
                props = contato.get("properties", {})
                status = "Lead encontrado"
                lead_id = contato.get("id", "")
                lifecycle = props.get("lifecyclestage", "")
                obs = f"Empresa: {props.get('company', '')}"
            else:
                status = "Novo lead"
        else:
            status = "Erro na API"
            obs = res.text

        # Atualiza as colunas G, H, I, J
        aba.update_cell(i+2, 7, status)
        aba.update_cell(i+2, 8, lead_id)
        aba.update_cell(i+2, 9, lifecycle)
        aba.update_cell(i+2, 10, obs)
