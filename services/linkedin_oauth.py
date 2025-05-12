import requests
import streamlit as st
from urllib.parse import urlencode

# Credenciais do LinkedIn
CLIENT_ID = st.secrets["LINKDIN_CLIENT_ID"]  # Substitua com seu Client ID
CLIENT_SECRET = st.secrets["LINKDIN_CLIENT_SECRET"]  # Substitua com seu Client Secret
REDIRECT_URI = st.secrets["LINKDIN_REDIRECT_URL"]  # Substitua com seu URI de redirecionamento

# URL de autorização do LinkedIn
AUTHORIZATION_URL = 'https://www.linkedin.com/oauth/v2/authorization'
TOKEN_URL = 'https://www.linkedin.com/oauth/v2/accessToken'

def gerar_url_autorizacao():
    """
    Gera a URL para redirecionar o usuário ao LinkedIn para autenticação
    """
    params = {
        'response_type': 'code',
        'client_id': CLIENT_ID,
        'redirect_uri': REDIRECT_URI,
        'scope': 'r_liteprofile w_member_social r_organization_social',  # Escopos necessários
        'state': 'unique_state_string',  # Use um valor único para proteção CSRF
    }
    return f"{AUTHORIZATION_URL}?{urlencode(params)}"

def obter_access_token(authorization_code):
    """
    Troca o Authorization Code pelo Access Token
    """
    data = {
        'grant_type': 'authorization_code',
        'code': authorization_code,
        'redirect_uri': REDIRECT_URI,
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET
    }
    response = requests.post(TOKEN_URL, data=data)
    if response.status_code == 200:
        return response.json().get('access_token')
    else:
        raise Exception(f"Erro ao obter o access token: {response.status_code} - {response.text}")
