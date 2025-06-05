import requests
import streamlit as st

ROCKETREACH_API_KEY = "197c58ck5cf775e09dfdd12eccb7423a66d2741d"
BASE_URL = "https://api.rocketreach.co/v1/api/lookupProfile"

def buscar_perfil_rocketreach(nome=None, email=None):
    headers = {
        "Authorization": f"Bearer {ROCKETREACH_API_KEY}"
    }

    if email:
        payload = {"email": email}
    elif nome:
        payload = {"name": nome}
    else:
        return None, "⚠️ Forneça um nome ou e-mail."

    response = requests.get(BASE_URL, params=payload, headers=headers)

    if response.status_code == 200:
        data = response.json()
        return data, None
    else:
        return None, f"❌ Status {response.status_code}: {response.text}"
