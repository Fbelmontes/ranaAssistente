import streamlit as st
import requests

def gerar_token_component():
    st.subheader("🔐 Gerar Access Token HubSpot")

    code = st.text_input("Cole aqui o `code` gerado pela URL da autorização")

    if st.button("Gerar Token"):
        if not code:
            st.warning("⚠️ Você precisa colar o code!")
            return

        with st.spinner("Trocando código por token..."):
            url = "https://api.hubapi.com/oauth/v1/token"
            data = {
                "grant_type": "authorization_code",
                "client_id": st.secrets["HUBSPOT_CLIENT_ID"],
                "client_secret": st.secrets["HUBSPOT_CLIENT_SECRET"],
                "redirect_uri": "https://ranaassistente.streamlit.app/",
                "code": code
            }
            headers = {"Content-Type": "application/x-www-form-urlencoded"}

            response = requests.post(url, data=data, headers=headers)

            if response.status_code == 200:
                tokens = response.json()
                st.success("✅ Token gerado com sucesso!")
                st.json(tokens)
                # Aqui podemos salvar em Sheets, arquivo, ou exibir apenas
            else:
                st.error("❌ Erro ao gerar token")
                st.text(response.text)
