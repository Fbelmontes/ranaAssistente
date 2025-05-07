import requests
import os

def trocar_code_por_token(code):
    url = "https://api.hubapi.com/oauth/v1/token"
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }

    data = {
        "grant_type": "authorization_code",
        "client_id": "b57c8418-dd11-4075-92bc-12489ee69f5d",
        "client_secret": "152a8b5c-e5b9-4497-a086-bc22d40aac38",
        "redirect_uri": "https://app.hubspot.com/oauth/authorize?client_id=b57c8418-dd11-4075-92bc-12489ee69f5d&redirect_uri=https://ranaassistente.streamlit.app/&scope=crm.objects.contacts.write%20crm.objects.marketing_events.read%20crm.objects.marketing_events.write%20oauth%20crm.objects.contacts.read",
        "code": code
    }

    response = requests.post(url, data=data, headers=headers)
    return response.json()

def renovar_token(refresh_token):
    url = "https://api.hubapi.com/oauth/v1/token"

    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }

    data = {
        "grant_type": "refresh_token",
        "client_id": st.secrets["HUBSPOT_CLIENT_ID"],
        "client_secret": st.secrets["HUBSPOT_CLIENT_SECRET"],
        "refresh_token": refresh_token
    }

    response = requests.post(url, headers=headers, data=data)
    return response.json()