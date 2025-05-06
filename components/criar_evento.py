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
        else:
            st.error("⚠️ O evento foi criado, mas a resposta da API está incompleta ou inválida.")

            try:
                if isinstance(resultado, dict):
                    st.json(resultado)
                elif isinstance(resultado, str):
                    import json
                    st.json(json.loads(resultado))
                else:
                    st.text(str(resultado))
            except Exception as e:
                st.text("Erro ao exibir resposta:")
                st.text(str(e))
                st.text(str(resultado))
