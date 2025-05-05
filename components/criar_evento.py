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

    if "evento_id_criado" not in st.session_state:
        st.session_state.evento_id_criado = None

    if st.button("Criar Evento"):
        dt_inicio = datetime.combine(inicio, hora_inicio).isoformat() + "Z"
        dt_fim = datetime.combine(fim, hora_fim).isoformat() + "Z"

        evento_id = criar_evento(nome, tipo, dt_inicio, dt_fim)
        st.session_state.evento_id_criado = evento_id

    if st.session_state.evento_id_criado:
        st.success("🎉 Evento criado com sucesso!")
        st.markdown(f"**🆔 ID do Evento:** `{st.session_state.evento_id_criado}`")
        st.caption("Use esse ID ao importar os leads para associá-los ao evento.")


