import requests
import streamlit as st

# Mapeamento das listas do Trello
LISTAS_TRELLO = {
    "BACKLOG RANA": "683da6577bcdfdcc2c22845c",
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
    "#9fc5e8": "64f78b58415ea65cb19073bd",  # Azul → Social Media
    "#f4cccc": "64f78b58415ea65cb19073b8",  # Rosa claro → Email/Newsletter
    "#f9cb9c": "67a66c956376c9941b825a97",  # Laranja → Pronto para produção
    "#d9d2e9": "64f78b58415ea65cb19073c5",  # Roxo claro → E-book, Report, etc.
    "#ead1dc": "64f78b58415ea65cb19073c7",  # Rosa escuro → Outros
    "#cfe2f3": "64fb7df6b0fe23614739456c",  # Azul céu → Ads
    "#b6d7a8": "66f5c1b036179ec660ac6359",  # Verde claro → Eventos
    "#ffe599": "66f5c1b036179ec660ac6365",  # Amarelo claro → Material de Conversão
    "#f6b26b": "68345669acf396379018804c",  # Laranja médio → Podcast
    "#c9daf8": "64fb900abb77971554145a62",  # Verde limão claro → Site
    "#a4c2f4": "67f9479df5d76c543a67c72e",  # Roxo médio → E-book
    "#6fa8dc": "64f78b58415ea65cb19073c0",  # Azul escuro → Analytics
    "#e06666": "66197f6c5b237211e70c8159",  # Vermelho claro → ABM
    "#cc0000": "6645259a8ebe198fbc0f8c59",  # Vermelho → Santander
    "#674ea7": "65044ce03ea504f11c5b55cb",  # Roxo escuro → Cases
}


# Credenciais do Trello
API_KEY = st.secrets["API_TRELLO"]
TOKEN = st.secrets["TOKEN_TRELLO"]


def criar_card(titulo, descricao, data, lista_id, cor_hex=None):
    url = "https://api.trello.com/1/cards"

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
            st.info(f"🎯 Aplicando etiqueta: {cor_formatada} → {etiqueta_id}")
        else:
            st.warning(f"⚠️ Cor sem mapeamento: {cor_hex}")

    headers = {
        "Content-Type": "application/json"
    }

    # DEBUG
    st.json(payload)

    response = requests.post(url, json=payload, headers=headers)

    if response.status_code == 200:
        return response.json()["id"]
    else:
        st.error(f"❌ Erro Trello: {response.text}")
        raise Exception(f"Erro ao criar card: {response.text}")

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

def atualizar_descricao_card(card_id, novo_texto):
    """
    Adiciona texto ao final da descrição existente do card.
    """
    url_get = f"https://api.trello.com/1/cards/{card_id}"
    params = {
        "key": API_KEY,
        "token": TOKEN,
        "fields": "desc"
    }

    response = requests.get(url_get, params=params)
    if response.status_code != 200:
        raise Exception(f"Erro ao obter descrição atual do card: {response.text}")

    descricao_atual = response.json().get("desc", "")
    nova_descricao = f"{descricao_atual.strip()}\n{novo_texto.strip()}"

    url_put = f"https://api.trello.com/1/cards/{card_id}"
    update_params = {
        "key": API_KEY,
        "token": TOKEN,
        "desc": nova_descricao
    }

    r = requests.put(url_put, params=update_params)
    if r.status_code != 200:
        raise Exception(f"Erro ao atualizar descrição do card {card_id}: {r.text}")

def anexar_texto_na_descricao(card_id, texto_adicional):
    """
    Atualiza a descrição de um card do Trello, mantendo o conteúdo anterior e adicionando novo texto ao final.
    """
    url_get = f"https://api.trello.com/1/cards/{card_id}"
    params = {
        "key": API_KEY,
        "token": TOKEN
    }
    response_get = requests.get(url_get, params=params)
    if response_get.status_code != 200:
        raise Exception(f"Erro ao buscar descrição atual: {response_get.text}")

    descricao_atual = response_get.json().get("desc", "")
    nova_descricao = descricao_atual.strip() + "\n\n📎 Briefing Recebido:\n" + texto_adicional.strip()

    url_put = f"https://api.trello.com/1/cards/{card_id}"
    response_put = requests.put(url_put, params=params | {"desc": nova_descricao})
    if response_put.status_code != 200:
        raise Exception(f"Erro ao atualizar descrição: {response_put.text}")

