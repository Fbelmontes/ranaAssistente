import streamlit as st
from services.linkedin_oauth import gerar_url_autorizacao, obter_access_token
from services.linkedin_api import buscar_dados_empresa_linkedin

def linkedin_integration_component():
    st.title("🔗 Integração com LinkedIn")

    # Passo 1: Redirecionar para o LinkedIn para obter o código de autorização
    if "access_token" not in st.session_state:
        auth_url = gerar_url_autorizacao()
        st.markdown(f"[Clique aqui para conectar sua conta do LinkedIn]({auth_url})")

    # Passo 2: Após a autorização, o LinkedIn redireciona com um código
    authorization_code = st.text_input("Insira o código de autorização (após login no LinkedIn):")

    if authorization_code:
        try:
            access_token = obter_access_token(authorization_code)
            st.session_state.access_token = access_token
            st.success("Autenticação bem-sucedida! Agora você pode buscar dados da empresa.")

        except Exception as e:
            st.error(f"Erro ao obter o token de acesso: {e}")

    # Passo 3: Consultar dados da empresa
    if "access_token" in st.session_state:
        empresa = st.text_input("Digite o nome da empresa (ex: 'Google'):")
        if empresa:
            dados_empresa = buscar_dados_empresa_linkedin(empresa, st.session_state.access_token)
            if "erro" in dados_empresa:
                st.error(dados_empresa["erro"])
            else:
                st.json(dados_empresa)
