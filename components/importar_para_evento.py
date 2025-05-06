import streamlit as st
from services.hubspot_event_api import importar_leads_para_evento

def importar_para_evento_component():
    st.subheader("📥 Importar Leads direto para Evento de Marketing")

    event_id = st.text_input("ID do evento (event_id):")
    external_event_id = st.text_input("External Event ID (ex: summit-2025)")

    arquivo_csv = st.file_uploader("Selecione o CSV com os leads", type=["csv"])

    if st.button("Importar para o Evento"):
        if not event_id or not external_event_id or not arquivo_csv:
            st.warning("Preencha todos os campos e selecione um arquivo.")
            return

        with st.spinner("Importando leads..."):
            resultados = importar_leads_para_evento(event_id, external_event_id, arquivo_csv)

            sucesso = [r for r in resultados if r[1]]
            falha = [r for r in resultados if not r[1]]

            st.success(f"{len(sucesso)} leads importados com sucesso!")
            if falha:
                st.error(f"{len(falha)} falharam:")
                for email, _ in falha:
                    st.markdown(f"- {email}")
