import streamlit as st
from datetime import datetime
from services.hubspot_event_api import criar_evento_marketing_api

def criar_evento_component():
    st.subheader("📅 Criar Evento de Marketing na HubSpot")

    nome = st.text_input("Nome do Evento")
    data = st.date_input("Data do Evento")
    hora_inicio = st.time_input("Hora de Início")
    hora_fim = st.time_input("Hora de Término")
    descricao = st.text_area("Descrição do Evento", "")
    url = st.text_input("Link do Evento (opcional)", "")

    if st.button("Criar Evento"):
        inicio_iso = datetime.combine(data, hora_inicio).isoformat() + "Z"
        fim_iso = datetime.combine(data, hora_fim).isoformat() + "Z"

        resultado = criar_evento_marketing_api(nome, inicio_iso, fim_iso, descricao, url)

        if "erro" in resultado:
            st.error("❌ Erro ao criar evento:")
            st.text(resultado["erro"])
        else:
            st.success("✅ Evento criado com sucesso!")
            st.markdown(f"**Nome:** {resultado['nome']}")
            st.markdown(f"**ID:** `{resultado['id']}`")
            st.markdown(f"**externalEventId:** `{resultado['externalEventId']}`")
