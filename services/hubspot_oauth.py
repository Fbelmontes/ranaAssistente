import requests
import streamlit as st

def renovar_token_automaticamente():
    url = "https://api.hubapi.com/oauth/v1/token"

    data = {
        "grant_type": "refresh_token",
        "client_id": st.secrets["HUBSPOT_CLIENT_ID"],
        "client_secret": st.secrets["HUBSPOT_CLIENT_SECRET"],
        "refresh_token": st.secrets["HUBSPOT_REFRESH_TOKEN"]
    }

    headers = {"Content-Type": "application/x-www-form-urlencoded"}

    response = requests.post(url, data=data, headers=headers)

    if response.status_code == 200:
        novo_token = response.json()
        return novo_token["access_token"]
    else:
        st.error("❌ Erro ao renovar token.")
        st.text(response.text)
        return None
