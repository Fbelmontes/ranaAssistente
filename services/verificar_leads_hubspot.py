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
                "properties": ["email", "lifecyclestage", "company", "firstname", "lastname", "linkedin", "jobtitle"],
                "limit": 5
            }

            filtros = []

            if email:
                payload["filterGroups"].append({
                    "filters": [{"propertyName": "email", "operator": "EQ", "value": email}]
                })
            else:
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

                if not resultados:
                    status = "Novo lead"
                else:
                    matches = []
                    for contato in resultados:
                        props = contato.get("properties", {})
                        # Verifica se nome, sobrenome e empresa batem
                        if (
                            nome.lower() in props.get("firstname", "").lower()
                            and sobrenome.lower() in props.get("lastname", "").lower()
                            and empresa.lower() in props.get("company", "").lower()
                        ):
                            matches.append(contato)

                    if email:
                        status = "Match exato"
                        contato = resultados[0]
                    elif len(matches) == 1:
                        status = "Match exato"
                        contato = matches[0]
                    elif len(matches) > 1:
                        status = "Possível match"
                        obs = "; ".join([
                            f"Empresa: {c['properties'].get('company','')}, ID: {c['id']}, Email: {c['properties'].get('email','')}"
                            for c in matches
                        ])
                        lead_id = ", ".join([c['id'] for c in matches])
                        lifecycle = matches[0]['properties'].get("lifecyclestage", "")
                        email_hubspot = matches[0]['properties'].get("email", "")
                        aba.update(f"G{i+2}:K{i+2}", [[status, lead_id, lifecycle, obs, email_hubspot]])
                        continue
                    else:
                        # Nenhum match 100% confiável
                        contato = resultados[0]
                        status = "Possível match"

                    props = contato.get("properties", {})
                    lead_id = contato.get("id", "")
                    lifecycle = props.get("lifecyclestage", "")
                    email_hubspot = props.get("email", "")
                    obs = f"Empresa: {props.get('company', '')} | Cargo: {props.get('jobtitle', '')}"

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
                print(f"Erro ao registrar falha: {erro_interno}")
            continue
