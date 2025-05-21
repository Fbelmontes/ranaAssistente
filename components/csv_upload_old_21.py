import streamlit as st
import pandas as pd
import requests
from services.hubspot_oauth import renovar_token_automaticamente
from datetime import datetime

def upload_leads_para_evento():
    st.subheader("📥 Enviar Leads para Evento")

    eventos = {
        "🚀 [BR] 2025.05.10 - Live - Websummit - Online - Linkedin": "430200305978",
        "🚀 [BR] 2025.05.08 - Inovabra Habitat - Liderança como potencia de transformação (presencial)": "430080653739",
        "🚀 [GLOBAL] 13-15.05.2025 - Leads Informatica World 2025 - Presencial": "430148874827",
        "🚀 [BR] 17.06.2025 - Agentes de IA: o desafio de governar o imprevisível - Live": "431162995823",
        "🚀 TESTE": "428556741234"
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
                # 🔐 Link fixo via secrets
        URL_FIXA_CSV = st.secrets["LEADS_MEMORIA"]

        if st.button("🔄 Atualizar Leads da Planilha Google"):
            try:
                st.session_state.df_leads = pd.read_csv(URL_FIXA_CSV)
                st.session_state["ultima_atualizacao"] = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                st.success("✅ Leads atualizados com sucesso!")
                st.rerun()
            except Exception as e:
                st.error(f"Erro ao carregar os leads: {e}")

        # 🕒 Exibe última atualização, se houver
        if "ultima_atualizacao" in st.session_state:
            st.info(f"🕒 Última atualização: {st.session_state['ultima_atualizacao']}")
        

    # 🧠 Se tiver df salvo, exibe preview e botão
    if st.session_state.df_leads is not None:
        st.markdown("### Pré-visualização dos Leads")
        st.dataframe(st.session_state.df_leads.head())

        if st.button("Enviar para o Make"):
            access_token = renovar_token_automaticamente()

            if not access_token:
                st.error("❌ Não foi possível gerar o token de acesso.")
                return

            leads = (
                st.session_state.df_leads
                .fillna("")  # remove NaNs
                .astype(str)  # força todos os campos a string
                .to_dict(orient="records")
            )

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