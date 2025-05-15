import streamlit as st
from services.linkedin_api import obter_eventos_organizacao
from services.google_sheets import salvar_na_planilha_leads

def consultar_eventos_component():
    st.title("📅 Consultar Eventos e Participantes LinkedIn")

    # Obter o Access Token do LinkedIn
    access_token = st.session_state.get('access_token', None)

    if access_token:
        # Buscar eventos da organização
        eventos = obter_eventos_organizacao(access_token)
        
        if "erro" in eventos:
            st.error(eventos["erro"])
        else:
            st.success("Eventos encontrados!")
            st.json(eventos)  # Exibe os eventos encontrados

            # Extraímos os leads de cada evento (isso depende dos dados disponíveis)
            leads_data = []  # Aqui você adiciona a lógica para coletar os dados dos leads
            
            # Exemplo simples de preenchimento de dados de leads
            for evento in eventos.get("events", []):
                leads_data.append({
                    "nome": "Lead Teste",  # Aqui você ajusta com os dados reais dos participantes
                    "email": "lead@exemplo.com",
                    "empresa": "Empresa Exemplo"
                })
            
            # Botão para salvar os dados em uma planilha
            if st.button("Salvar Leads na Planilha"):
                spreadsheet_id = st.secrets["GOOGLE_SHEET_ID"]  # ID da planilha
                resultado = salvar_na_planilha_leads(leads_data, spreadsheet_id)
                if "sucesso" in resultado:
                    st.success(resultado["sucesso"])
                else:
                    st.error(resultado["erro"])
    else:
        st.warning("Você precisa se autenticar primeiro!")
