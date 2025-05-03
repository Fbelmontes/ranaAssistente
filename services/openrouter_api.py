import requests
import streamlit as st

OPENROUTER_API_KEY = st.secrets["OPENROUTER_API_KEY"]

def responder_pergunta(prompt):
    url = "https://openrouter.ai/api/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://ranaassistente.streamlit.app",  # obrigatório para Streamlit Cloud
        "X-Title": "RANA Assistente"
    }

    body = {
        "model": "openchat/openchat-3.5",  # modelo gratuito e estável
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ],
        "temperature": 0.2
    }

    try:
        response = requests.post(url, headers=headers, json=body)
        if response.status_code == 200:
            return response.json()["choices"][0]["message"]["content"]
        else:
            st.error(f"Erro ao consultar OpenRouter: {response.status_code}")
            st.text(response.text)  # mostra motivo detalhado do erro
            return None
    except Exception as e:
        st.error(f"Erro de conexão com OpenRouter: {str(e)}")
        return None

def listar_modelos_disponiveis():
    url = "https://openrouter.ai/api/v1/models"
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}"
    }

    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            modelos = response.json().get("data", [])
            return [m["id"] for m in modelos]
        else:
            st.error(f"Erro ao consultar modelos: {response.status_code}")
            st.text(response.text)
            return []
    except Exception as e:
        st.error(f"Erro ao buscar modelos: {str(e)}")
        return []