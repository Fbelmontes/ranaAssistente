import requests
import streamlit as st
from urllib.parse import urlencode
import uuid

# Credenciais do LinkedIn
CLIENT_ID = st.secrets["LINKDIN_CLIENT_ID"]  # Client ID do LinkedIn
CLIENT_SECRET = st.secrets["LINKDIN_CLIENT_SECRET"]  # Client Secret do LinkedIn
REDIRECT_URI = st.secrets["LINKDIN_REDIRECT_URL"]  # URI de redirecionamento configurada no LinkedIn Developer Portal

# URL de autorização do LinkedIn
AUTHORIZATION_URL = 'https://www.linkedin.com/oauth/v2/authorization'
TOKEN_URL = 'https://www.linkedin.com/oauth/v2/accessToken'

def gerar_url_autorizacao():
    """
    Gera a URL para redirecionar o usuário ao LinkedIn para autenticação
    """
    # Gerar um valor único para 'state' para proteção contra CSRF
    state = str(uuid.uuid4())
    
    params = {
        'response_type': 'code',  # Solicita o Authorization Code
        'client_id': CLIENT_ID,
        'redirect_uri': REDIRECT_URI,
        'scope': 'r_liteprofile w_member_social r_events',  # Escopos necessários
        'state': state  # Parâmetro de segurança para evitar CSRF
    }
    
    # Retorna a URL de autorização para redirecionar o usuário
    return f"{AUTHORIZATION_URL}?{urlencode(params)}"

def obter_access_token(authorization_code):
    """
    Troca o Authorization Code pelo Access Token
    """
    data = {
        'grant_type': 'authorization_code',  # O tipo de grant que estamos usando
        'code': authorization_code,  # Código de autorização obtido após a autenticação
        'redirect_uri': REDIRECT_URI,  # O mesmo URI de redirecionamento
        'client_id': CLIENT_ID,  # Client ID do LinkedIn
        'client_secret': CLIENT_SECRET  # Client Secret do LinkedIn
    }
    
    # Fazendo a requisição POST para obter o Access Token
    response = requests.post(TOKEN_URL, data=data)
    
    if response.status_code == 200:
        # Retorna o Access Token se a requisição for bem-sucedida
        return response.json().get('access_token')
    else:
        # Se não for bem-sucedido, levanta uma exceção com o erro
        raise Exception(f"Erro ao obter o access token: {response.status_code} - {response.text}")

