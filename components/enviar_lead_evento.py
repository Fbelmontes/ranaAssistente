import streamlit as st
from services.hubspot_event_api import enviar_lead_para_evento

def enviar_lead_evento_component():
    st.subheader("📩 Enviar Lead para Evento de Marketing")

    st.markdown("Preencha os dados do lead para associar ao evento.")

    access_token = st.text_input("Access Token OAuth")  # você pode depois puxar dos secrets
    external_event_id = st.text_input("ID do Evento (externalEventId)")
    email = st.text_input("Email do Lead")
    first_name = st.text_input("Primeiro Nome")
    last_name = st.text_input("Último Nome")

    if st.button("📤 Enviar Lead"):
        resultado = enviar_lead_para_evento(access_token, external_event_id, email, first_name, last_name)

        if resultado["sucesso"]:
            st.success("✅ Lead enviado com sucesso!")
            st.json(resultado["resposta"])
        else:
            st.error(f"❌ Erro: {resultado['erro']}")


