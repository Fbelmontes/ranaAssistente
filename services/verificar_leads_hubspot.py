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
            sobrenome = linha.get("Sobrenome", "").strip()
            empresa = linha.get("Empresa", "").strip()
            email = linha.get("E-mail", "").strip()
            linkedin = linha.get("LinkedIn", "").strip()
            cargo = linha.get("Cargo", "").strip()

            status = "Não encontrado"
            lead_id = ""
            lifecycle = ""
            obs = ""
            email_hubspot = ""

            payload = {
                "filterGroups": [],
                "properties": [
                    "email", "lifecyclestage", "company", "firstname", "lastname",
                    "linkedin", "jobtitle"
                ],
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
                if sobrenome:
                    filtros.append({"propertyName": "lastname", "operator": "CONTAINS_TOKEN", "value": sobrenome})
                if empresa:
                    filtros.append({"propertyName": "company", "operator": "CONTAINS_TOKEN", "value": empresa})
                if cargo:
                    filtros.append({"propertyName": "jobtitle", "operator": "CONTAINS_TOKEN", "value": cargo})
                if linkedin:
                    filtros.append({"propertyName": "linkedin", "operator": "CONTAINS_TOKEN", "value": linkedin})

                if filtros:
                    payload["filterGroups"].append({"filters": filtros})
                else:
                    # Nada para pesquisar
                    aba.update(f"G{i+2}:K{i+2}", [["Dados insuficientes", "", "", "", ""]])
                    continue

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
                    obs = f"Empresa: {props.get('company', '')} | Cargo: {props.get('jobtitle', '')}"
                else:
                    status = "Novo lead"
            else:
                status = "Erro na API"
                obs = res.text

            aba.update(f"H{i+2}:L{i+2}", [[
                str(status or ""),
                str(lead_id or ""),
                str(lifecycle or ""),
                str(obs or ""),
                str(email_hubspot or "")
            ]])

        except Exception as e:
            erro_msg = f"Erro na linha {i+2}: {e}"
            print(erro_msg)
            try:
                aba.update(f"H{i+2}:L{i+2}", [["Erro", "", "", erro_msg[:500], ""]])
            except Exception as erro_interno:
                print(f"Erro ao registrar falha na planilha: {erro_interno}")
            continue
