import streamlit as st
from services.hubspot_oauth import renovar_token

def renovar_token_component():
    st.subheader("🔄 Renovar Token de Acesso")

    refresh_token = st.text_input("Cole seu Refresh Token aqui:")

    if st.button("🔁 Renovar Token"):
        with st.spinner("Renovando token..."):
            resultado = renovar_token(refresh_token)

            if "access_token" in resultado:
                novo_token = resultado["access_token"]
                st.success("✅ Novo Access Token gerado!")
                st.code(novo_token, language="text")

                # Opcional: armazenar na sessão
                st.session_state["access_token"] = novo_token
            else:
                st.error("❌ Erro ao renovar token:")
                st.json(resultado)
