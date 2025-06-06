import requests
from difflib import SequenceMatcher
from services.google_sheets import conectar_sheets
from services.hubspot_oauth import renovar_token_automaticamente

ABA_VERIFICAR = "Verificar_Leads"

def similaridade(a, b):
    return SequenceMatcher(None, a.lower(), b.lower()).ratio()

def pontuar_lead(lead, nome, sobrenome, empresa, cargo, linkedin):
    props = lead.get("properties", {})
    score = 0
    detalhes = []

    if nome and props.get("firstname") and similaridade(nome, props["firstname"]) > 0.8:
        score += 1
        detalhes.append("Nome")
    if sobrenome and props.get("lastname") and similaridade(sobrenome, props["lastname"]) > 0.8:
        score += 1
        detalhes.append("Sobrenome")
    if empresa and props.get("company") and similaridade(empresa, props["company"]) > 0.75:
        score += 1
        detalhes.append("Empresa")
    if cargo and props.get("jobtitle") and similaridade(cargo, props["jobtitle"]) > 0.75:
        score += 0.5
        detalhes.append("Cargo")
    if linkedin and props.get("linkedin") and linkedin.strip() == props["linkedin"].strip():
        score += 2
        detalhes.append("LinkedIn exato")

    return score, ", ".join(detalhes)

def buscar_leads_na_base():
    token = renovar_token_automaticamente()
    aba = conectar_sheets().worksheet(ABA_VERIFICAR)
    dados = aba.get_all_records()

    updates = []
    for i, linha in enumerate(dados):
        nome = linha.get("Nome", "").strip()
        sobrenome = linha.get("Sobrenome", "").strip()
        empresa = linha.get("Empresa", "").strip()
        cargo = linha.get("Cargo", "").strip()
        linkedin = linha.get("Linkedin", "").strip()

        filtros = []
        if nome:
            filtros.append({"propertyName": "firstname", "operator": "CONTAINS_TOKEN", "value": nome})
        if sobrenome:
            filtros.append({"propertyName": "lastname", "operator": "CONTAINS_TOKEN", "value": sobrenome})
        if empresa:
            filtros.append({"propertyName": "company", "operator": "CONTAINS_TOKEN", "value": empresa})

        payload = {
            "filterGroups": [{"filters": filtros}],
            "properties": ["firstname", "lastname", "email", "company", "lifecyclestage", "linkedin", "jobtitle"],
            "limit": 10
        }

        res = requests.post(
            "https://api.hubapi.com/crm/v3/objects/contacts/search",
            headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"},
            json=payload
        )

        if res.status_code != 200:
            updates.append([i + 2, "Erro API", "", "", res.text, ""])
            continue

        resultado = res.json().get("results", [])
        if not resultado:
            updates.append([i + 2, "Novo Lead", "", "", "Nenhum resultado", ""])
            continue

        melhores = []
        melhor_score = 0

        for lead in resultado:
            score, detalhes = pontuar_lead(lead, nome, sobrenome, empresa, cargo, linkedin)
            if score > melhor_score:
                melhores = [(lead, score, detalhes)]
                melhor_score = score
            elif score == melhor_score:
                melhores.append((lead, score, detalhes))

        if melhor_score == 0:
            updates.append([i + 2, "Novo Lead", "", "", "Sem correspondência relevante", ""])
        elif len(melhores) > 1:
            obs_text = "; ".join([f"ID: {m[0]['id']} ({m[2]})" for m in melhores])
            emails = "; ".join([m[0].get("properties", {}).get("email", "") for m in melhores])
            updates.append([i + 2, "Possível duplicata", "", "", obs_text, emails])
        else:
            lead = melhores[0][0]
            props = lead.get("properties", {})
            status = "Match exato" if melhor_score >= 3 else "Possível match"
            updates.append([
                i + 2,
                status,
                lead.get("id", ""),
                props.get("lifecyclestage", ""),
                f"Empresa: {props.get('company','')} | {melhores[0][2]}",
                props.get("email", "")
            ])

    # Atualiza colunas H a L (5 colunas): Status, ID, Lifecycle, Observações, E-mail HubSpot
    for update in updates:
        linha, status, lead_id, lifecycle, obs, email = update
        try:
            aba.batch_update([{
                "range": f"H{linha}:L{linha}",
                "values": [[status, lead_id, lifecycle, obs, email]]
            }])
        except Exception as e:
            print(f"Erro ao atualizar linha {linha}: {e}")
