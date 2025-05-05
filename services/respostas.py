import json
import requests
import streamlit as st
from services.memoria import ler_toda_memoria
from services.openrouter_api import responder_pergunta


OPENROUTER_KEY = st.secrets["OPENROUTER_API_KEY"]

#def responder_com_contexto(pergunta):
#    memoria = ler_toda_memoria()
#    base_conhecimento = json.dumps(memoria, ensure_ascii=False)

#    prompt = f"""
#Você é a RANA, uma assistente com acesso a dados sobre empresas.

#Responda com base nos dados abaixo (não invente nada):

#{base_conhecimento}

#Pergunta: {pergunta}
#Resposta:
#"""
#    return responder_pergunta(prompt)

def responder_com_contexto(pergunta):
    memoria = ler_toda_memoria()
    if not memoria:
        return "Ainda não aprendi nada."

    contexto = "\n\n".join(memoria)
    prompt = f"""
Aja como um assistente especialista e responda com base apenas nos conteúdos abaixo.

Contexto aprendido:
\"\"\"{contexto}\"\"\"

Pergunta: {pergunta}
Resposta:
"""

    headers = {
        "Authorization": f"Bearer {OPENROUTER_KEY}",
        "Content-Type": "application/json"
    }

    body = {
        "model": "mistral/mistral-7b-instruct",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.7
    }

    response = requests.post("https://openrouter.ai/api/v1/chat/completions", json=body, headers=headers)

    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"]
    else:
        st.error(f"Erro ao consultar OpenRouter: {response.status_code}")
        st.text(response.text)
        return "Desculpe, não consegui encontrar nada."

