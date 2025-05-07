import streamlit as st
from services.make_webhook import enviar_lead_para_evento

def enviar_lead_evento_component():
    st.subheader("📤 Enviar Lead para Evento de Marketing")

    col1, col2 = st.columns(2)
    with col1:
        first_name = st.text_input("Nome")
        last_name = st.text_input("Sobrenome")
    with col2:
        email = st.text_input("Email")
        external_event_id = st.text_input("ID externo do Evento", help="Use o campo 'externalEventId' gerado na criação do evento")

    if st.button("Enviar Lead"):
        if not all([first_name, last_name, email, external_event_id]):
            st.warning("⚠️ Preencha todos os campos antes de enviar.")
        else:
            lead = {
                "firstName": first_name,
                "lastName": last_name,
                "email": email,
                "externalEventId": external_event_id
            }

            resultado = enviar_lead_para_evento(lead)

            if "erro" in resultado:
                st.error(f"❌ Erro: {resultado['erro']}")
            else:
                st.success("✅ Lead enviado com sucesso!")
