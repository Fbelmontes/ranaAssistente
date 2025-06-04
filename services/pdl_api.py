import requests
import streamlit as st

PDL_API_KEY = st.secrets["KEY_PPD"]

def buscar_perfis_pdl(nome=None, email=None):
    url = "https://api.peopledatalabs.com/v5/person/search"
    headers = {
        "X-api-key": PDL_API_KEY
    }

    if not nome and not email:
        return {"erro": "⚠️ Insira pelo menos o nome ou o e-mail."}

    params = {
        "size": 3,  # retorna os 3 melhores perfis
        "pretty": "true"
    }

    # Criação da query no estilo PDL
    query = {}
    if nome:
        query["full_name"] = nome
    if email:
        query["email"] = email

    params["query"] = str(query).replace("'", '"')  # formato JSON no param

    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200:
        return response.json()
    else:
        return {"erro": f"Status {response.status_code}: {response.text}"}