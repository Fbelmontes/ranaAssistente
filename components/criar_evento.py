import streamlit as st
from services.hubspot_event_api import criar_evento_marketing
from datetime import datetime

def criar_evento_component():
    st.subheader("📅 Criar Novo Evento de Marketing")

    nome = st.text_input("Nome do evento")
    data_inicio = st.date_input("Data do evento")
    hora_inicio = st.time_input("Hora de início")
    hora_fim = st.time_input("Hora de término")

    if st.button("Criar evento"):
        inicio_iso = datetime.combine(data_inicio, hora_inicio).isoformat() + "Z"
        fim_iso = datetime.combine(data_inicio, hora_fim).isoformat() + "Z"

        resultado = criar_evento_marketing(nome, inicio_iso, fim_iso)

        if resultado and "id" in resultado:
            st.success(f"✅ Evento criado com sucesso!")
            st.markdown(f"**Nome:** {resultado['nome']}")
            st.markdown(f"**ID:** `{resultado['id']}`")

            if "erro" in resultado:
                st.warning(resultado["erro"])
        else:
            st.error("⚠️ O evento foi criado, mas a resposta da API está incompleta ou inválida.")
            try:
                st.json(resultado)
            except Exception:
                st.text(str(resultado))
