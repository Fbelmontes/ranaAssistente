import requests
import streamlit as st

def enviar_evento_para_make(dados_evento):
    url = st.secrets["MAKE_WEBHOOK_EVENTO_URL"]

    try:
        response = requests.post(url, json=dados_evento)

        if response.status_code == 200:
            return {"sucesso": True, "resposta": response.json() if response.text else "OK"}
        else:
            return {"sucesso": False, "erro": response.text}
    except Exception as e:
        return {"sucesso": False, "erro": str(e)}
