import requests
import pandas as pd
import streamlit as st
import io

HUBSPOT_TOKEN = st.secrets["HUBSPOT_API_TOKEN"]
HEADERS = {
    "Authorization": f"Bearer {HUBSPOT_TOKEN}",
    "Content-Type": "application/json"
}

def criar_evento_marketing(nome_evento, inicio, fim):
    url = "https://api.hubapi.com/marketing/v3/marketing-events/events"

    body = {
        "eventName": nome_evento,
        "eventType": "WEBINAR",
        "startDateTime": inicio,         # Ex: "2025-06-10T18:00:00Z"
        "endDateTime": fim,              # Ex: "2025-06-10T20:00:00Z"
        "eventOrganizer": "mjv",         # <- Obrigatório
        "externalAccountId": "rana-assistente",   # <- Obrigatório e fixo
        "externalEventId": nome_evento.lower().replace(" ", "-")  # opcional, mas bom para rastrear
    }

    response = requests.post(url, headers=HEADERS, json=body)

    if response.status_code == 201:
        evento = response.json()
        return {
            "id": evento["id"],
            "nome": evento["eventName"]
        }
    else:
        st.error("Erro ao criar evento")
        st.text(response.text)
        return None

def listar_eventos():
    url = "https://api.hubapi.com/marketing/v3/marketing-events/external-events"
    response = requests.get(url, headers=HEADERS)

    if response.status_code == 200:
        return response.json().get("results", [])
    else:
        st.error("Erro ao listar eventos")
        st.text(response.text)
        return []

def registrar_participante(event_id, email, external_event_id):
    url = f"https://api.hubapi.com/marketing/v3/marketing-events/events/{event_id}/registrations"
    
    body = {
        "email": email,
        "registrationStatus": "REGISTERED",
        "externalAccountId": "rana-assistente",
        "externalContactId": email,
        "externalEventId": external_event_id
    }

    response = requests.post(url, headers=HEADERS, json=body)

    if response.status_code == 204:
        return True
    else:
        st.error("Erro ao registrar participante no evento")
        st.text(response.text)
        return False

def importar_leads_para_evento(event_id, external_event_id, csv_file):
    
    df = pd.read_csv(io.StringIO(csv_file.getvalue().decode("utf-8")))

    resultados = []

    for _, row in df.iterrows():
        email = row.get("email")
        if email:
            sucesso = registrar_participante(event_id, email, external_event_id)
            resultados.append((email, sucesso))

    return resultados

