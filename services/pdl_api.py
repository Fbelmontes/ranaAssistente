import requests
import streamlit as st

PDL_API_KEY = st.secrets["KEY_PPD"]

def buscar_perfil_pdl(nome, email=None, empresa=None):
    url = "https://api.peopledatalabs.com/v5/person/enrich"
    headers = {
        "X-api-key": PDL_API_KEY
    }
    params = {
        "name": nome,
        "pretty": "true"
    }

    if email:
        params["email"] = email
    if empresa:
        params["company"] = empresa

    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200:
        return response.json()
    else:
        return {"erro": f"Status {response.status_code}: {response.text}"}
