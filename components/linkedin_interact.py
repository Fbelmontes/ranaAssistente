import streamlit as st
import requests
from services.openrouter_api import responder_pergunta

def linkedin_interaction_component():
    st.subheader("🤖 Curtir e Comentar com Engajamento")

    post_urn = st.text_input("Cole o URN do post (ex: urn:li:activity:123456789)")
    post_texto = st.text_area("Cole aqui o conteúdo do post (ou uma descrição do assunto)")

    if st.button("Gerar comentário e interagir"):
        if post_urn and post_texto:
            with st.spinner("RANA está gerando um comentário engajador..."):
                prompt = f"""
Crie um comentário curto e engajador para um post do LinkedIn com o seguinte conteúdo:

\"\"\"{post_texto}\"\"\"

O comentário deve:
- Ser profissional
- Trazer empatia ou reforço positivo
- Incluir emojis e hashtags se fizer sentido
- Ser humano e gerar engajamento

Resposta:
"""
                comentario = responder_pergunta(prompt)

                payload = {
                    "urn": post_urn,
                    "comentario": comentario
                }

                webhook_url = st.secrets["MAKE_WEBHOOK_URL"]
                response = requests.post(webhook_url, json=payload)

                if response.status_code == 200:
                    st.success("Interação enviada com sucesso! 💬")
                    st.markdown(f"**Comentário gerado:** {comentario}")
                else:
                    st.error("Erro ao enviar para o Make")
                    st.text(response.text)
        else:
            st.warning("Preencha o URN e o conteúdo do post.")
