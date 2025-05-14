import streamlit as st
from services.linkedin_oauth import gerar_url_autorizacao, obter_access_token, obter_codigo_autorizacao

def linkedin_auth_component():
    st.title("🔗 Autenticação com LinkedIn")

    # Passo 1: Gerar a URL de autorização para o LinkedIn
    auth_url = gerar_url_autorizacao()
    st.markdown(f"Para autorizar o acesso ao LinkedIn, [clique aqui]({auth_url}) e conceda permissão à RANA.")
    
    # Passo 2: Captura do código de autorização após o redirecionamento
    authorization_code = obter_codigo_autorizacao()

    if authorization_code:
        try:
            # Troca o código de autorização pelo Access Token
            access_token = obter_access_token(authorization_code)
            st.session_state.access_token = access_token
            st.success("Autenticação bem-sucedida! Agora você pode acessar dados da sua conta LinkedIn.")
        except Exception as e:
            st.error(f"Erro ao obter o token de acesso: {e}")
    else:
        st.info("Aguardando o código de autorização... Clique no link acima para autorizar a RANA.")
