import streamlit as st
import pandas as pd
import requests

def upload_leads_para_evento():
    st.subheader("📥 Enviar Leads para Evento")

    # Opções visíveis com valores reais por trás
    eventos = {
        "🚀 [BR] 2025.05.10 - Live - Websummit - Online - Linkedin": "427754195285",
        "🚀 TESTE": "427796696458",
        "🚀 Demo Day MJV 2025": "45678901"
    }

    evento_nome = st.selectbox("Selecione o evento", list(eventos.keys()))
    evento_id = eventos[evento_nome]  # ID real oculto

    arquivo = st.file_uploader("Envie o CSV com os leads", type=["csv"])

    if evento_id and arquivo:
        df = pd.read_csv(arquivo)

        st.write("Pré-visualização:")
        st.dataframe(df.head())

        if st.button("Enviar para o Make"):
            leads = df.to_dict(orient="records")

            payload = {
                "evento_id": evento_id,
                "leads": leads
            }

            webhook_url = st.secrets["MAKE_EVENT_WEBHOOK_URL"]
            response = requests.post(webhook_url, json=payload)

            if response.status_code == 200:
                st.success("Leads enviados com sucesso para o evento!")
            else:
                st.error("Erro ao enviar para o Make.")
                st.text(response.text)
