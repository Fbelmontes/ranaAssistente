import requests
import streamlit as st

# Certifique-se de que sua chave da OpenRouter está salva nos segredos como:
# st.secrets["OPENROUTER_API_KEY"]
OPENROUTER_API_KEY = st.secrets["OPENROUTER_API_KEY"]

def responder_pergunta(prompt):
    url = "https://openrouter.ai/api/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://ranaassistente.streamlit.app",
        "X-Title": "RANA Assistente IA"
    }

    body = {
        "model": "openrouter/openchat-3.5",
        "messages": [
            {
                "role": "system",
                "content": "Você é a RANA, uma assistente que responde com base em registros de empresas salvos em memória. Nunca invente nada. Seja objetiva."
            },
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
            return None
    except Exception as e:
        st.error(f"Erro de conexão com OpenRouter: {str(e)}")
        return None
