import streamlit as st
import requests

def renovar_token_component():
    st.subheader("🔄 Renovar Access Token HubSpot")

    refresh_token = st.text_input("Cole aqui o `refresh_token` atual")

    if st.button("Renovar Token"):
        if not refresh_token:
            st.warning("⚠️ Por favor, insira o refresh token.")
            return

        with st.spinner("Renovando token..."):
            url = "https://api.hubapi.com/oauth/v1/token"
            data = {
                "grant_type": "refresh_token",
                "client_id": st.secrets["HUBSPOT_CLIENT_ID"],
                "client_secret": st.secrets["HUBSPOT_CLIENT_SECRET"],
                "refresh_token": refresh_token
            }
            headers = {"Content-Type": "application/x-www-form-urlencoded"}

            response = requests.post(url, data=data, headers=headers)

            if response.status_code == 200:
                tokens = response.json()
                st.success("✅ Novo token gerado com sucesso!")
                st.json(tokens)
            else:
                st.error("❌ Erro ao renovar o token")
                st.text(response.text)
