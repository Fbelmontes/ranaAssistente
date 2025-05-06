import requests
import streamlit as st

HUBSPOT_TOKEN = st.secrets["HUBSPOT_API_TOKEN"]
HEADERS = {
    "Authorization": f"Bearer {HUBSPOT_TOKEN}",
    "Content-Type": "application/json"
}

def criar_evento(nome_evento, tipo_evento, inicio, fim, external_id=None):
    url = "https://api.hubapi.com/marketing/v3/marketing-events/events"

    payload = {
        "eventName": nome_evento,
        "eventType": tipo_evento.upper(),  # Ex: WEBINAR, CONFERENCE
        "startDateTime": inicio,
        "endDateTime": fim,
        "externalEventId": external_id or nome_evento.replace(" ", "_").lower(),
        "eventOrganizer": "MJV Innovation",  # 👈 Aqui você pode personalizar
        "externalAccountId": "rana-assistente"
    }

    response = requests.post(url, json=payload, headers=HEADERS)

    if response.status_code in [200, 201]:
        return response.json().get("id")
    else:
        st.error("Erro ao criar evento")
        st.text(response.text)
        return None

def listar_eventos():
    url = "https://api.hubapi.com/marketing/v3/marketing-events/events"
    response = requests.get(url, headers=HEADERS)

    if response.status_code == 200:
        return response.json().get("results", [])
    else:
        st.error("Erro ao listar eventos")
        st.text(response.text)
        return []