import requests
import streamlit as st

ROCKETREACH_API_KEY = st.secrets["ROCK_API"]  # Substitua aqui

def buscar_perfil_rocketreach(nome=None, email=None, empresa=None):
    url = "https://api.rocketreach.co/v1/api/lookupProfile"
    params = {"api_key": ROCKETREACH_API_KEY}

    if email:
        params["email"] = email
    elif nome and empresa:
        params["name"] = nome
        params["current_employer"] = empresa
    else:
        return {"erro": "❌ Para buscar por nome, você deve informar também a empresa."}

    response = requests.get(url, params=params)

    if response.status_code == 200:
        return response.json()
    else:
        return {"erro": f"Status {response.status_code}: {response.text}"}