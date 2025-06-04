import requests
import streamlit as st

ROCKETREACH_API_KEY = st.secrets["ROCK_API"]  # Substitua aqui

def buscar_perfil_rocketreach(nome=None, email=None):
    url = "https://api.rocketreach.co/v1/api/lookupProfile"
    params = {"api_key": ROCKETREACH_API_KEY}

    if email:
        params["email"] = email
    elif nome:
        params["name"] = nome
    else:
        return {"erro": "❌ Informe pelo menos o nome ou o e-mail."}

    response = requests.get(url, params=params)

    if response.status_code == 200:
        return response.json()
    else:
        return {"erro": f"Status {response.status_code}: {response.text}"}
