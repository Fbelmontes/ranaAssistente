import streamlit as st
from services.make_webhook import enviar_evento_para_make
from datetime import datetime

def enviar_evento_make_component():
    st.subheader("🚀 Enviar Evento para o Make")

    nome = st.text_input("Nome do evento")
    data = st.date_input("Data do evento")
    hora_inicio = st.time_input("Hora de início")
    hora_fim = st.time_input("Hora de término")
    descricao = st.text_area("Descrição do evento (opcional)", "")
    link_evento = st.text_input("Link do evento (opcional)", "")

    if st.button("Enviar para o Make"):
        dt_inicio = datetime.combine(data, hora_inicio).isoformat() + "Z"
        dt_fim = datetime.combine(data, hora_fim).isoformat() + "Z"

        dados_evento = {
            "eventName": nome,
            "eventType": "WEBINAR",
            "startDateTime": dt_inicio,
            "endDateTime": dt_fim,
            "eventOrganizer": "mjv",
            "externalAccountId": "rana-assistente",
            "externalEventId": nome.lower().replace(" ", "-"),
            "eventDescription": descricao,
            "eventUrl": link_evento,
            "eventCancelled": False,
            "eventCompleted": False,
            "customProperties": []
        }

        resultado = enviar_evento_para_make(dados_evento)

        if resultado["sucesso"]:
            st.success("✅ Evento enviado com sucesso para o Make!")
            st.json(resultado["resposta"])
        else:
            st.error("❌ Erro ao enviar para o Make:")
            st.text(resultado["erro"])
