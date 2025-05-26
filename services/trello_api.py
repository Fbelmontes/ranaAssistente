import requests
import streamlit as st

# Mapeamento das listas
LISTAS_TRELLO = {
    "BACKLOG": "67a289a7a2f8f98484a418ea",
    "PARA SEMANA": "67a289ae54d6edf31151b464",
    "EVENTOS": "67a289b37cfedcee3f26bbb3",
    "CONTEUDO": "67a289bbe7777e8d075aa30b",
    "DESIGN": "67a289c238280ce45d863a84",
    "AUTOMAÇÃO": "67a289ce9c2365cbd484a45b",
    "PARA PUBLICAR": "67a289e2b597e915ad706199",
    "CONCLUIDO": "67a289e7f598f7040d09d38e",
    "STUCK": "67a289ef69c2b08592bcbb5a"
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
        "due": f"{data}T12:00:00.000Z",
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
        "due": f"{data}T12:00:00.000Z",
        "idList": LISTAS_TRELLO.get(lista_nome.upper(), "")
    }
    r = requests.put(url, params=params)
    if r.status_code != 200:
        raise Exception(f"Erro ao atualizar card {card_id}: {r.text}")
