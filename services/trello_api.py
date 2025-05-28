import requests
import streamlit as st

# Mapeamento das listas do Trello
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

# Mapeamento das cores da planilha para as etiquetas do Trello
MAPA_CORES_TRELLO = {
    "#9fc5e8": "67a2899a3eccd70031a43a54",  # azul → Post Redes Sociais
    "#fff2cc": "67a2899a3eccd70031a43a50",  # amarelo → Ebooks e Reports
    "#b6d7a8": "67a2899a3eccd70031a43a4f",  # verde → (sem nome)
    "#f9cb9c": "67a2899a3eccd70031a43a51",  # laranja → Pronto para produção
    "#d9d2e9": "67a2899a3eccd70031a43a53",  # roxo → (sem nome)
    "#e06666": "67a2899a3eccd70031a43a52",  # vermelho → REVISÃO
}

# Credenciais do Trello
API_KEY = st.secrets["API_TRELLO"]
TOKEN = st.secrets["TOKEN_TRELLO"]

def criar_card(titulo, descricao, data, lista_nome, cor_hex=None):
    url = f"https://api.trello.com/1/cards"
    params = {
        "key": API_KEY,
        "token": TOKEN,
        "name": titulo,
        "desc": descricao,
        "due": data,
        "idList": LISTAS_TRELLO.get(lista_nome.upper(), "")
    }

    # Adiciona etiqueta se a cor existir no mapeamento
    if cor_hex and cor_hex.lower() in MAPA_CORES_TRELLO:
        params["idLabels"] = MAPA_CORES_TRELLO[cor_hex.lower()]

    r = requests.post(url, params=params)
    if r.status_code == 200:
        return r.json()["id"]
    else:
        raise Exception(f"Erro ao criar card: {r.text}")

def atualizar_card(card_id, titulo, descricao, data, lista_nome, cor_hex=None):
    url = f"https://api.trello.com/1/cards/{card_id}"
    params = {
        "key": API_KEY,
        "token": TOKEN,
        "name": titulo,
        "desc": descricao,
        "due": data,
        "idList": LISTAS_TRELLO.get(lista_nome.upper(), "")
    }

    # Atualiza etiqueta se a cor estiver no mapeamento
    if cor_hex and cor_hex.lower() in MAPA_CORES_TRELLO:
        params["idLabels"] = MAPA_CORES_TRELLO[cor_hex.lower()]

    r = requests.put(url, params=params)
    if r.status_code != 200:
        raise Exception(f"Erro ao atualizar card {card_id}: {r.text}")

def buscar_cards_da_lista(id_lista):
    url = f"https://api.trello.com/1/lists/{id_lista}/cards"
    params = {
        "key": API_KEY,
        "token": TOKEN
    }
    r = requests.get(url, params=params)
    if r.status_code == 200:
        return r.json()
    else:
        raise Exception(f"Erro ao buscar cards da lista {id_lista}: {r.text}")

def buscar_todos_os_cards():

    url = f"https://api.trello.com/1/boards/{st.secrets['ID_BOARD_TRELLO']}/cards"
    params = {
        "key": API_KEY,
        "token": TOKEN
    }
    r = requests.get(url, params=params)
    if r.status_code == 200:
        return r.json()
    else:
        raise Exception(f"Erro ao buscar todos os cards: {r.text}")

def buscar_cards_do_board():
    url = f"https://api.trello.com/1/boards/{st.secrets['ID_BOARD_TRELLO']}/cards"
    params = {
        "key": API_KEY,
        "token": TOKEN
    }
    r = requests.get(url, params=params)
    if r.status_code == 200:
        return r.json()
    else:
        raise Exception(f"Erro ao buscar cards do board: {r.text}")