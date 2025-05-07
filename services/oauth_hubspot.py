import streamlit as st
import requests
import urllib.parse

# Carregue essas variáveis de forma segura (ex: via secrets)
CLIENT_ID = st.secrets["HUBSPOT_CLIENT_ID"]
CLIENT_SECRET = st.secrets["HUBSPOT_CLIENT_SECRET"]
REDIRECT_URI = st.secrets["HUBSPOT_REDIRECT_URI"]

AUTH_URL = "https://app.hubspot.com/oauth/authorize"
TOKEN_URL = "https://api.hubapi.com/oauth/v1/token"

def gerar_url_autenticacao():
    params = {
        "client_id": CLIENT_ID,
        "redirect_uri": REDIRECT_URI,
        "scope": "marketing.events.read marketing.events.write",
        "response_type": "code"
    }
    return f"{AUTH_URL}?{urllib.parse.urlencode(params)}"

def trocar_codigo_por_token(code):
    data = {
        "grant_type": "authorization_code",
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "redirect_uri": REDIRECT_URI,
        "code": code
    }

    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }

    response = requests.post(TOKEN_URL, data=data, headers=headers)
    return response.json()
