import streamlit as st
from services.linkedin_api import obter_eventos_organizacao, obter_detalhes_evento

def consultar_eventos_component():
    st.title("📅 Consultar Eventos e Participantes LinkedIn")

    # Obter o Access Token do LinkedIn
    access_token = st.session_state.get('access_token', None)

    if access_token:
        # Pedir o ID da organização
        organization_id = st.text_input("Digite o ID da sua organização LinkedIn:")

        if organization_id:
            eventos = obter_eventos_organizacao(access_token, organization_id)

            if "erro" in eventos:
                st.error(eventos["erro"])
            else:
                st.success("Eventos encontrados!")
                st.json(eventos)  # Exibe os eventos encontrados

                # Aqui você pode detalhar os eventos ou enviar para o Make
                if st.button("Detalhes do Evento"):
                    # Aqui pegamos o ID do evento selecionado para obter detalhes
                    event_id = st.selectbox("Escolha um evento", [evento['id'] for evento in eventos.get("elements", [])])
                    
                    if event_id:
                        detalhes_evento = obter_detalhes_evento(access_token, event_id)
                        if "erro" in detalhes_evento:
                            st.error(detalhes_evento["erro"])
                        else:
                            st.json(detalhes_evento)  # Exibe os detalhes do evento

                # Enviar os dados dos eventos para o Make
                if st.button("Enviar Dados para o Make"):
                    make_webhook_url = st.secrets["MAKE_WEBHOOK_URL"]  # URL do Webhook do Make
                    resultado = enviar_dados_para_make(eventos, make_webhook_url)
                    if "sucesso" in resultado:
                        st.success(resultado["sucesso"])
                    else:
                        st.error(resultado["erro"])
    else:
        st.warning("Você precisa se autenticar primeiro!")
