import requests
import streamlit as st

def enviar_evento_para_make(dados_evento):
    url = st.secrets["MAKE_WEBHOOK_EVENTO_URL"]

    try:
        response = requests.post(url, json=dados_evento)

        if response.status_code == 200:
            try:
                json_resposta = response.json()
            except Exception:
                json_resposta = response.text or "OK"

            return {"sucesso": True, "resposta": json_resposta}
        else:
            return {"sucesso": False, "erro": response.text}

    except Exception as e:
        return {"sucesso": False, "erro": str(e)}

def enviar_lead_para_evento(lead):
    url = st.secrets["MAKE_WEBHOOK_LEAD_EVENTO"]

    try:
        response = requests.post(url, json=lead)

        if response.status_code == 200:
            return {"sucesso": True, "resposta": response.text}
        else:
            return {"erro": response.text}
    except Exception as e:
        return {"erro": str(e)}