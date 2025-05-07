import requests
import os

def trocar_code_por_token(code):
    url = "https://api.hubapi.com/oauth/v1/token"
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }

    data = {
        "grant_type": "authorization_code",
        "client_id": os.getenv("HUBSPOT_CLIENT_ID"),
        "client_secret": os.getenv("HUBSPOT_CLIENT_SECRET"),
        "redirect_uri": os.getenv("HUBSPOT_REDIRECT_URI"),
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
        "client_id": "b57c8418-dd11-4075-92bc-12489ee69f5d",
        "client_secret": "152a8b5c-e5b9-4497-a086-bc22d40aac38",
        "refresh_token": refresh_token
    }

    response = requests.post(url, headers=headers, data=data)
    return response.json()