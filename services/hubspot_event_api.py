import requests
import streamlit as st

HUBSPOT_TOKEN = st.secrets["HUBSPOT_API_TOKEN"]
HEADERS = {
    "Authorization": f"Bearer {HUBSPOT_TOKEN}",
    "Content-Type": "application/json"
}

def criar_ou_atualizar_contato(email, firstname=None, lastname=None):
    url = "https://api.hubapi.com/crm/v3/objects/contacts"

    data = {
        "properties": {
            "email": email,
            "firstname": firstname or "",
            "lastname": lastname or ""
        }
    }

    response = requests.post(url, json=data, headers=HEADERS)

    # Se já existir, pode retornar erro 409. Vamos ignorar isso.
    if response.status_code in [200, 201, 409]:
        return True
    else:
        st.error(f"Erro ao criar contato: {response.status_code}")
        st.text(response.text)
        return False

def registrar_no_evento(event_id, email):
    url = f"https://api.hubapi.com/marketing/v3/marketing-events/events/{event_id}/registrations"

    data = {
        "email": email,
        "registrationStatus": "REGISTERED",
        "externalAccountId": "rana-assistente",
        "externalContactId": email,
        "externalEventId": str(event_id)
    }

    response = requests.post(url, json=data, headers=HEADERS)

    if response.status_code in [200, 201]:
        return True
    else:
        st.error(f"Erro ao registrar no evento: {response.status_code}")
        st.text(response.text)
        return False

def processar_leads_para_evento(df, event_id):
    resultados = []
    for _, row in df.iterrows():
        email = row.get("email")
        nome = row.get("nome", "")
        sobrenome = row.get("sobrenome", "")

        if not email:
            continue

        if criar_ou_atualizar_contato(email, nome, sobrenome):
            registrado = registrar_no_evento(event_id, email)
            resultados.append({"email": email, "registrado": registrado})
    return resultados
