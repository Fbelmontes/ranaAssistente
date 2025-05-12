import requests
from urllib.parse import urlencode
import streamlit as st

CLIENT_ID = st.secrets["LINKDIN_CLIENT_ID"]  # Substitua pelo seu Client ID
CLIENT_SECRET = st.secrets["LINKDIN_CLIENT_SECRET"]  # Substitua pelo seu Client Secret
REDIRECT_URI = st.secrets["LINKDIN_REDIRECT_URL"]  # O URI de redirecionamento após login

AUTHORIZATION_URL = "https://www.linkedin.com/oauth/v2/authorization"
TOKEN_URL = "https://www.linkedin.com/oauth/v2/accessToken"

# Função para gerar o link de autorização
def gerar_url_autorizacao():
    params = {
        "response_type": "code",
        "client_id": CLIENT_ID,
        "redirect_uri": REDIRECT_URI,
        "scope": "r_liteprofile w_member_social",  # Remova r_emailaddress se não for necessário
        "state": "unique_state_string",  # Use um estado único para evitar CSRF
    }
    url = f"{AUTHORIZATION_URL}?{urlencode(params)}"
    return url

# Função para obter o access token usando o authorization code
def obter_access_token(authorization_code):
    data = {
        "grant_type": "authorization_code",
        "code": st.secrets["LINKDIN_CODE_AUTHORIZATION"],
        "redirect_uri": REDIRECT_URI,
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
    }
    response = requests.post(TOKEN_URL, data=data)
    if response.status_code == 200:
        return response.json().get("access_token")
    else:
        raise Exception(f"Erro ao obter o access token: {response.status_code}")

