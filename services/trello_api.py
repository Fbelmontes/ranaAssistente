import requests
import streamlit as st

# Mapeamento das listas
LISTAS_TRELLO = {
    "BACKLOG": "64f78d0c362c5efc717c8b4f",
    "A FAZER": "66f5c26aa9bb4fe4a1adb29d",
    "EVENTOS": "67a6643e09ad4d568223789e",
    "CONTEÚDO": "67a6644476298d0728598d30",
    "DESIGN": "67a66449fca49c7b784bc10a",
    "AUTOMAÇÃO": "67a66457849350b6cbb3d5fd",
    "CRM": "67a6645b56b4b732b851eae4",
    "REVISÃO": "67a66465e78c374af458851e",
    "PRONTO PARA PUBLICAR": "67a6647736e2199ba0eed338",
    "CONCLUÍDO": "66f5c299135d99693f57d296",
    "STUCK": "64f78d8243294d54660ef714",
    "STUCK/PARADO": "64f78d8243294d54660ef714"
}

# Credenciais
API_KEY = st.secrets["API_TRELLO"]
TOKEN = st.secrets["TOKEN_TRELLO"]

def criar_card(titulo, descricao, data, lista_nome):
    url = f"https://api.trello.com/1/cards"
    params = {
        "key": API_KEY,
        "token": TOKEN,
        "name": titulo,
        "desc": descricao,
        "due": data,
        "idList": LISTAS_TRELLO.get(lista_nome.upper(), "")
    }
    r = requests.post(url, params=params)
    if r.status_code == 200:
        return r.json()["id"]
    else:
        raise Exception(f"Erro ao criar card: {r.text}")

def atualizar_card(card_id, titulo, descricao, data, lista_nome):
    url = f"https://api.trello.com/1/cards/{card_id}"
    params = {
        "key": API_KEY,
        "token": TOKEN,
        "name": titulo,
        "desc": descricao,
        "due": data,
        "idList": LISTAS_TRELLO.get(lista_nome.upper(), "")
    }
    r = requests.put(url, params=params)
    if r.status_code != 200:
        raise Exception(f"Erro ao atualizar card {card_id}: {r.text}")
