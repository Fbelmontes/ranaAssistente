import streamlit as st
import requests

def upload_csv_para_make():
    st.subheader("📤 Importar Leads via CSV")

    csv_file = st.file_uploader("Envie seu arquivo CSV com leads", type=["csv"])
    
    if csv_file is not None:
        st.success("Arquivo carregado com sucesso.")
        
        if st.button("Importar Leads"):
            with st.spinner("Enviando para a HubSpot..."):

                make_webhook_url = st.secrets["MAKE_WEBHOOK_URL"]
                files = {"file": (csv_file.name, csv_file.getvalue())}

                try:
                    response = requests.post(make_webhook_url, files=files)
                    if response.status_code == 200:
                        st.success("Leads enviados com sucesso para a HubSpot! ✅")
                    else:
                        st.error(f"Erro ao enviar: {response.status_code} - {response.text}")
                except Exception as e:
                    st.error(f"Erro na requisição: {e}")
