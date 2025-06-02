import requests
from services.google_sheets import conectar_sheets
from services.hubspot_oauth import renovar_token_automaticamente

PLANILHA_ID = "1YnX5Lg7eW6AXwSdo73SIwvlxc4fITwUw5mTPHlspSqA"
ABA_VERIFICAR = "Verificar_Leads"

def buscar_leads_na_base():
    # 1. Renova o token automaticamente
    access_token = renovar_token_automaticamente()

    # 2. Lê os dados da aba
    aba = conectar_sheets().worksheet(ABA_VERIFICAR)
    dados = aba.get_all_records()

    resultados = []

    for linha in dados:
        nome = linha.get("Nome", "")
        empresa = linha.get("Empresa", "")
        email = linha.get("E-mail", "")

        resultado = {
            "Status Pesquisa": "Não encontrado",
            "ID HubSpot": "",
            "Lifecycle Stage": "",
            "Observações": ""
        }

        if email:
            filtro = f"properties.email={email}"
        else:
            filtro = f"properties.firstname__icontains={nome}&properties.company__icontains={empresa}"

        url = f"https://api.hubapi.com/crm/v3/objects/contacts/search"
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }

        payload = {
            "filterGroups": [
                {
                    "filters": [
                        {
                            "propertyName": "email" if email else "firstname",
                            "operator": "EQ" if email else "CONTAINS_TOKEN",
                            "value": email if email else nome
                        }
                    ]
                }
            ],
            "properties": ["email", "lifecyclestage", "company"],
            "limit": 1
        }

        res = requests.post(url, headers=headers, json=payload)

        if res.status_code == 200:
            resultado_json = res.json()
            if resultado_json.get("results"):
                contato = resultado_json["results"][0]
                resultado["Status Pesquisa"] = "Lead encontrado"
                resultado["ID HubSpot"] = contato.get("id", "")
                props = contato.get("properties", {})
                resultado["Lifecycle Stage"] = props.get("lifecyclestage", "")
                resultado["Observações"] = "Encontrado via pesquisa HubSpot"
            else:
                resultado["Status Pesquisa"] = "Novo lead"
        else:
            resultado["Status Pesquisa"] = "Erro na API"
            resultado["Observações"] = res.text

        resultados.append(resultado)

    # Atualizar a aba com os resultados
    for idx, r in enumerate(resultados):
        aba.update_cell(idx + 2, 7, r["Status Pesquisa"])
        aba.update_cell(idx + 2, 8, r["ID HubSpot"])
        aba.update_cell(idx + 2, 9, r["Lifecycle Stage"])
        aba.update_cell(idx + 2, 10, r["Observações"])
