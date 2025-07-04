import streamlit as st
import requests

def url_input_component():
    st.subheader("🔗 Enviar URL para o n8n")

    url = st.text_input("Cole aqui a URL que deseja enviar:")

    # ⚠️ Substitua aqui pelo SEU Webhook de produção do n8n
    webhook_url = "https://fbelmonte95.app.n8n.cloud/webhook-test/209e02d6-8def-4ce5-9e49-6029d4a84f22"

    if st.button("🚀 Enviar para o n8n"):
        if url.strip():
            payload = {"url": url.strip()}
            try:
                response = requests.post(webhook_url, json=payload)
                if response.status_code == 200:
                    st.success("URL enviada com sucesso! ✅")
                else:
                    st.error(f"Erro ao enviar: {response.status_code} - {response.text}")
            except Exception as e:
                st.error(f"Erro na requisição: {e}")
        else:
            st.warning("Insira uma URL antes de enviar.")
