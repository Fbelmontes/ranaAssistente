import streamlit as st
from services.linkedin_oauth import gerar_url_autorizacao, obter_access_token
from services.linkedin_api import buscar_dados_empresa_linkedin

def linkedin_integration_component():
    st.title("🔗 Integração com LinkedIn")

    # Passo 1: Se o Access Token não estiver presente, mostre o link de autorização
    if "access_token" not in st.session_state:
        authorization_code = st.text_input("Insira o código de autorização do LinkedIn:")
        if authorization_code:
            try:
                access_token = obter_access_token(authorization_code)
                st.session_state.access_token = access_token
                st.success("Autenticação bem-sucedida! Agora você pode buscar dados da empresa.")
            except Exception as e:
                st.error(f"Erro ao obter o token de acesso: {e}")
        
    # Passo 2: Após autenticação, busque os dados da empresa
    if "access_token" in st.session_state:
        company_name = st.text_input("Digite o nome da empresa (ex: 'Google'):")
        if company_name:
            dados_empresa = buscar_dados_empresa_linkedin(company_name, st.session_state.access_token)
            if "erro" in dados_empresa:
                st.error(dados_empresa["erro"])
            else:
                st.json(dados_empresa)
