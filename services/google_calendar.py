from __future__ import print_function
import datetime
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# Escopo necessário
SCOPES = ['https://www.googleapis.com/auth/calendar']

def autenticar_google_calendar():
    creds = None
    token_path = "token_calendar.pickle"
    
    if os.path.exists(token_path):
        with open(token_path, 'rb') as token:
            creds = pickle.load(token)
    
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials_calendar.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open(token_path, 'wb') as token:
            pickle.dump(creds, token)

    service = build('calendar', 'v3', credentials=creds)
    return service

def verificar_eventos():
    service = autenticar_google_calendar()
    agora = datetime.datetime.utcnow().isoformat() + 'Z'
    
    eventos_result = service.events().list(
        calendarId='primary',
        timeMin=agora,
        maxResults=5,
        singleEvents=True,
        orderBy='startTime'
    ).execute()

    eventos = eventos_result.get('items', [])
    lista = []
    for evento in eventos:
        inicio = evento['start'].get('dateTime', evento['start'].get('date'))
        lista.append(f"{evento['summary']} - {inicio}")
    
    return lista if lista else ["Nenhum evento encontrado."]

def criar_evento(titulo, data_hora_inicio, data_hora_fim, convidados=[]):
    service = autenticar_google_calendar()
    
    evento = {
        'summary': titulo,
        'start': {
            'dateTime': data_hora_inicio,
            'timeZone': 'America/Sao_Paulo',
        },
        'end': {
            'dateTime': data_hora_fim,
            'timeZone': 'America/Sao_Paulo',
        },
        'attendees': [{'email': email} for email in convidados],
    }

    evento = service.events().insert(calendarId='primary', body=evento).execute()
    return f"Evento criado: {evento.get('htmlLink')}"
