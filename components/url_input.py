import streamlit as st
import requests

def url_input_component():
    st.subheader("🔗 Enviar URL para análise")

    url = st.text_input("Cole aqui a URL que deseja enviar:")
    webhook_url = "https://seu-webhook-do-n8n.n8n.cloud/webhook-url"  # Substitua pelo seu

    if st.button("🚀 Enviar para o n8n"):
        if url.strip() != "":
            payload = {"url": url}
            try:
                response = requests.post(webhook_url, json=payload)
                if response.status_code == 200:
                    st.success("URL enviada com sucesso! ✅")
                else:
                    st.error(f"Erro ao enviar: {response.status_code} - {response.text}")
            except Exception as e:
                st.error(f"Erro na requisição: {e}")
        else:
            st.warning("Por favor, insira uma URL válida.")
