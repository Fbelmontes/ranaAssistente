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
    "#ffff00": "67a2899a3eccd70031a43a52",  # vermelho → REVISÃO (duplicado)
}

# Credenciais do Trello
API_KEY = st.secrets["API_TRELLO"]
TOKEN = st.secrets["TOKEN_TRELLO"]


def criar_card(titulo, descricao, data, lista_id, cor_hex=None):
    url = f"https://api.trello.com/1/cards"

    payload = {
        "key": API_KEY,
        "token": TOKEN,
        "name": titulo,
        "desc": descricao,
        "due": data,
        "idList": lista_id
    }

    if cor_hex:
        cor_formatada = cor_hex.lower().strip()
        etiqueta_id = MAPA_CORES_TRELLO.get(cor_formatada)
        if etiqueta_id:
            payload["idLabels"] = [etiqueta_id]
            st.info(f"🎯 Enviando etiqueta ID {etiqueta_id} para '{titulo}'")
        else:
            st.warning(f"⚠️ Cor não encontrada no mapa: {cor_hex}")

    headers = {
        "Content-Type": "application/json"
    }

    r = requests.post(url, json=payload, headers=headers)

    if r.status_code == 200:
        return r.json()["id"]
    else:
        raise Exception(f"❌ Erro ao criar card: {r.text}")



def atualizar_card(card_id, titulo, descricao, data, lista_id, cor_hex=None):
    url = f"https://api.trello.com/1/cards/{card_id}"

    payload = {
        "key": API_KEY,
        "token": TOKEN,
        "name": titulo,
        "desc": descricao,
        "due": data,
        "idList": lista_id
    }

    if cor_hex:
        cor_formatada = cor_hex.lower().strip()
        etiqueta_id = MAPA_CORES_TRELLO.get(cor_formatada)
        if etiqueta_id:
            payload["idLabels"] = [etiqueta_id]
            st.info(f"🔁 Atualizando etiqueta no card '{titulo}' com ID {etiqueta_id}")
        else:
            st.warning(f"⚠️ Cor não mapeada para etiqueta: {cor_hex}")

    headers = {
        "Content-Type": "application/json"
    }

    r = requests.put(url, json=payload, headers=headers)

    if r.status_code != 200:
        raise Exception(f"❌ Erro ao atualizar card: {r.text}")


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


def buscar_cards_do_board(board_id):
    """
    Busca todos os cards de todas as listas dentro do board especificado.
    """
    url = f"https://api.trello.com/1/boards/{board_id}/cards"
    params = {
        "key": API_KEY,
        "token": TOKEN,
        "fields": "name,idList,due"
    }
    r = requests.get(url, params=params)
    if r.status_code == 200:
        return r.json()
    else:
        raise Exception(f"Erro ao buscar cards do board {board_id}: {r.text}")
