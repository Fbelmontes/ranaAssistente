import streamlit as st
import pandas as pd
import requests

def upload_csv_para_evento():
    st.subheader("📥 Enviar CSV com Leads para Evento")

    evento_id = st.text_input("ID do Evento no HubSpot")
    arquivo = st.file_uploader("Envie o CSV com os leads", type=["csv"])

    if evento_id and arquivo:
        df = pd.read_csv(arquivo)

        st.write("Prévia do CSV:")
        st.dataframe(df)

        if st.button("Enviar para Make"):
            leads = df.to_dict(orient="records")

            payload = {
                "evento_id": evento_id,
                "leads": leads
            }

            webhook_url = st.secrets["MAKE_WEBHOOK_URL"]

            response = requests.post(webhook_url, json=payload)

            if response.status_code == 200:
                st.success("Leads enviados com sucesso para o Make!")
            else:
                st.error("Erro ao enviar para Make.")
                st.text(response.text)
