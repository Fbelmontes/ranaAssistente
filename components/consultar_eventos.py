import streamlit as st
from services.linkedin_api import obter_eventos_sales_navigator

def consultar_eventos_component():
    st.title("📅 Consultar Eventos e Participantes LinkedIn")

    # Obter o Access Token do LinkedIn
    access_token = st.session_state.get('access_token', None)

    if access_token:
        # Buscar eventos da organização via Sales Navigator API
        organization_id = st.text_input("Digite o ID da sua organização LinkedIn:")
        
        if organization_id:
            eventos = obter_eventos_sales_navigator(access_token, organization_id)
        
            if "erro" in eventos:
                st.error(eventos["erro"])
            else:
                st.success("Eventos encontrados!")
                st.json(eventos)  # Exibe os eventos encontrados

                # Extraímos os leads de cada evento (isso depende dos dados disponíveis)
                leads_data = []  # Aqui você adiciona a lógica para coletar os dados dos leads
                
                # Exemplo simples de preenchimento de dados de leads (ajustar conforme a resposta da API)
                for evento in eventos.get("elements", []):  # Ajuste conforme a estrutura de resposta
                    leads_data.append({
                        "nome": evento.get("organizerName", "Nome Não Disponível"),
                        "email": evento.get("organizerEmail", "email@exemplo.com"),
                        "evento": evento.get("name", "Evento Não Disponível"),
                        "data": evento.get("startDate", "Data Não Disponível")
                    })
                
                # Enviar os dados para o Make via Webhook
                if st.button("Enviar Leads para o Make"):
                    make_webhook_url = st.secrets["MAKE_WEBHOOK_URL"]  # URL do Webhook do Make
                    resultado = enviar_dados_para_make(leads_data, make_webhook_url)
                    if "sucesso" in resultado:
                        st.success(resultado["sucesso"])
                    else:
                        st.error(resultado["erro"])
    else:
        st.warning("Você precisa se autenticar primeiro!")
