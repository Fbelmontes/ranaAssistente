from services.hubspot_event_api import enviar_lead_para_evento

access_token = st.secrets["HUBSPOT_ACCESS_TOKEN"]
external_event_id = st.text_input("ID do Evento (externalEventId)")
email = st.text_input("E-mail do lead")
first_name = st.text_input("Nome")
last_name = st.text_input("Sobrenome")

if st.button("Enviar Lead para o Evento"):
    resultado = enviar_lead_para_evento(access_token, external_event_id, email, first_name, last_name)
    if resultado["sucesso"]:
        st.success("✅ Lead enviado com sucesso!")
        st.json(resultado["resposta"])
    else:
        st.error(f"❌ Erro: {resultado['erro']}")
