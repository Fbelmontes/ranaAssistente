import streamlit as st
from services.hubspot_event_api import criar_evento
from datetime import datetime

def criar_evento_component():
    st.subheader("📅 Criar Evento de Marketing (HubSpot)")

    nome = st.text_input("Nome do Evento")
    tipo = st.selectbox("Tipo de Evento", ["WEBINAR", "WORKSHOP", "CONFERENCE", "OTHER"])

    col1, col2 = st.columns(2)
    with col1:
        inicio = st.date_input("Data de Início", format="YYYY-MM-DD")
        hora_inicio = st.time_input("Hora de Início")
    with col2:
        fim = st.date_input("Data de Fim", format="YYYY-MM-DD")
        hora_fim = st.time_input("Hora de Fim")

    if st.button("Criar Evento"):
        dt_inicio = datetime.combine(inicio, hora_inicio).isoformat() + "Z"
        dt_fim = datetime.combine(fim, hora_fim).isoformat() + "Z"

        evento_id = criar_evento(nome, tipo, dt_inicio, dt_fim)

        if evento_id:
            st.success(f"Evento criado com sucesso! ID: {evento_id}")
            st.code(evento_id)
