import requests
from services.google_sheets import conectar_sheets
from services.hubspot_oauth import renovar_token_automaticamente

ABA_VERIFICAR = "Verificar_Leads"

def buscar_leads_na_base():
    access_token = renovar_token_automaticamente()
    aba = conectar_sheets().worksheet(ABA_VERIFICAR)
    dados = aba.get_all_records()

    for i, linha in enumerate(dados):
        try:
            nome = linha.get("Nome", "").strip()
            empresa = linha.get("Empresa", "").strip()
            email = linha.get("E-mail", "").strip()

            status = "Não encontrado"
            lead_id = ""
            lifecycle = ""
            obs = ""
            email_hubspot = ""

            # Monta a payload da pesquisa
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

            # Faz a requisição à API do HubSpot
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
                    email_hubspot = props.get("email", "")
                    obs = f"Empresa: {props.get('company', '')}"
                else:
                    status = "Novo lead"
            else:
                status = "Erro na API"
                obs = res.text

            # Atualiza a planilha com conversão segura
            aba.update_cell(i+2, 7, str(status or ""))
            aba.update_cell(i+2, 8, str(lead_id or ""))
            aba.update_cell(i+2, 9, str(lifecycle or ""))
            aba.update_cell(i+2, 10, str(obs or ""))
            aba.update_cell(i+2, 11, str(email_hubspot or ""))

        except Exception as e:
            erro_msg = f"Erro na linha {i+2}: {e}"
            print(erro_msg)
            aba.update_cell(i+2, 7, "Erro")
            aba.update_cell(i+2, 10, erro_msg)
            continue
