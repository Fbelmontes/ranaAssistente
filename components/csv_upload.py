import streamlit as st
import pandas as pd
import requests
from services.hubspot_oauth import renovar_token_automaticamente

def upload_leads_para_evento():
    st.subheader("📥 Enviar Leads para Evento")

    eventos = {
        "🚀 [BR] 2025.05.10 - Live - Websummit - Online - Linkedin": "427754195285",
        "🚀 TESTE": "428046103560",
        "🚀 Demo Day MJV 2025": "45678901"
    }

    evento_nome = st.selectbox("Selecione o evento", list(eventos.keys()))
    evento_id = eventos[evento_nome]

    modo = st.radio("Como deseja importar os leads?", ["📎 Upload CSV", "🔗 Link Google Sheets CSV"])

    # 🔐 Inicia o estado se ainda não existir
    if "df_leads" not in st.session_state:
        st.session_state.df_leads = None

    if modo == "📎 Upload CSV":
        arquivo = st.file_uploader("Envie o arquivo CSV", type=["csv"])
        if arquivo is not None:
            try:
                st.session_state.df_leads = pd.read_csv(arquivo)
                st.success("✅ CSV carregado com sucesso!")
            except Exception as e:
                st.error(f"Erro ao ler o arquivo: {e}")

    elif modo == "🔗 Link Google Sheets CSV":
        url_csv = st.text_input("Cole o link público do Google Sheets (formato CSV):")
        if url_csv and st.button("Carregar Leads do Link"):
            try:
                st.session_state.df_leads = pd.read_csv(url_csv)
                st.success("✅ Leads carregados do link com sucesso!")
                st.experimental_rerun()  # 🔄 força recarregar a interface
            except Exception as e:
                st.error(f"Erro ao carregar o link: {e}")
        

    # 🧠 Se tiver df salvo, exibe preview e botão
    if st.session_state.df_leads is not None:
        st.markdown("### Pré-visualização dos Leads")
        st.dataframe(st.session_state.df_leads.head())

        if st.button("Enviar para o Make"):
            access_token = renovar_token_automaticamente()

            if not access_token:
                st.error("❌ Não foi possível gerar o token de acesso.")
                return

            leads = st.session_state.df_leads.to_dict(orient="records")

            payload = {
                "evento_id": evento_id,
                "leads": leads,
                "access_token": access_token
            }

            webhook_url = st.secrets["MAKE_EVENT_WEBHOOK_URL"]
            response = requests.post(webhook_url, json=payload)

            if response.status_code == 200:
                st.success("✅ Leads enviados com sucesso para o Make!")
                st.session_state.df_leads = None  # limpa após envio
            else:
                st.error("❌ Erro ao enviar os dados.")
                st.text(response.text)
