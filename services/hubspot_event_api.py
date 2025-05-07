import requests
import pandas as pd
import streamlit as st
import io
import time

HUBSPOT_TOKEN = st.secrets["HUBSPOT_API_TOKEN"]
HEADERS = {
    "Authorization": f"Bearer {HUBSPOT_TOKEN}",
    "Content-Type": "application/json"
}

def criar_evento_marketing_api(nome, dt_inicio, dt_fim, descricao=None, url_evento=None):
    endpoint = "https://api.hubapi.com/marketing/v3/marketing-events/events"

    body = {
        "eventName": nome,
        "eventType": "WEBINAR",
        "startDateTime": dt_inicio,
        "endDateTime": dt_fim,
        "eventOrganizer": "mjv",
        "externalAccountId": "rana-assistente",
        "externalEventId": nome.lower().replace(" ", "-"),
        "eventDescription": descricao or "Evento criado via RANA",
        "eventUrl": url_evento or "https://mjv.com.br",
        "eventCancelled": False,
        "eventCompleted": False,
        "customProperties": []
    }

    try:
        response = requests.post(endpoint, headers=HEADERS, json=body)

        evento = response.json()

        if response.status_code in [200, 201] and "objectId" in evento:
            return {
                "id": evento["objectId"],
                "externalEventId": body["externalEventId"],
                "nome": body["eventName"]
            }
        else:
            return {"erro": evento}
    except Exception as e:
        return {"erro": str(e)}

def criar_evento_marketing(access_token, event_name, start_datetime, end_datetime, external_event_id):
    url = "https://api.hubapi.com/marketing/v3/marketing-events"

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    body = {
        "eventName": event_name,
        "eventType": "WEBINAR",  # pode ser 'WEBINAR', 'CONFERENCE', etc
        "startDateTime": start_datetime,
        "endDateTime": end_datetime,
        "eventOrganizer": "mjv",
        "eventDescription": "Criado automaticamente pela RANA",
        "eventUrl": "https://mjv.com.br",
        "eventCancelled": False,
        "eventCompleted": False,
        "externalEventId": external_event_id,
        "externalAccountId": "rana-assistente"  # ID fixo para agrupar seus eventos
    }

    response = requests.post(url, headers=headers, json=body)

    if response.status_code == 200:
        return {"sucesso": True, "resposta": response.json()}
    else:
        return {
            "sucesso": False,
            "erro": response.text,
            "status": response.status_code
        }

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

def validar_evento_ativo(event_id):
    url = f"https://api.hubapi.com/marketing/v3/marketing-events/events/{event_id}"
    
    for tentativa in range(5):  # tenta até 5 vezes
        response = requests.get(url, headers=HEADERS)

        if response.status_code == 200:
            evento = response.json()
            status = evento.get("eventStatus", "UNKNOWN")
            if status == "ACTIVE":
                return True
            else:
                time.sleep(2)  # espera 2 segundos e tenta de novo
        else:
            st.warning("Não consegui consultar o status do evento.")
            st.text(response.text)
            break

    return False

def enviar_lead_para_evento(access_token, external_event_id, email, first_name, last_name):
    """
    Envia um lead individual para um evento de marketing no HubSpot.
    """
    url = "https://api.hubapi.com/marketing/v3/marketing-events/attendance"

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    body = {
        "externalAccountId": "rana-assistente",  # esse valor pode ser qualquer identificador do seu sistema
        "externalEventId": external_event_id,    # o ID do evento que a RANA criou
        "attendee": {
            "email": email,
            "firstName": first_name,
            "lastName": last_name,
            "registrationStatus": "registered"   # status obrigatório: 'registered'
        }
    }

    response = requests.post(url, headers=headers, json=body)

    if response.status_code == 200:
        return {"sucesso": True, "resposta": response.json()}
    else:
        return {
            "sucesso": False,
            "erro": response.text,
            "status": response.status_code
        }
