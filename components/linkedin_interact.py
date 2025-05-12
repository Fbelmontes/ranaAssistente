import streamlit as st
import requests
from services.openrouter_api import responder_pergunta

def linkedin_interaction_component():
    st.subheader("🤖 Curtir, Comentar e Compartilhar (se for da MJV)")

    post_urn = st.text_input("Cole o URN do post (ex: urn:li:activity:123456789)")
    post_texto = st.text_area("Cole aqui o conteúdo do post (ou uma descrição do assunto)")

    if st.button("Verificar e interagir com o post"):
        if post_urn and post_texto:
            # Verifica se é da MJV (simplesmente por conter "MJV" no texto)
            acao = "curtir_comentar"  # ação padrão

            if "MJV" in post_texto.upper():  # Ajuste para verificar melhor
                acao = "curtir_comentar_compartilhar"
            
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
                    "comentario": comentario,
                    "acao": acao
                }

                webhook_url = st.secrets["MAKE_WEBHOOK_URL_LINKEDIN"]  # Certifique-se de que o URL está correto
                response = requests.post(webhook_url, json=payload)

                if response.status_code == 200:
                    st.success("Interação enviada com sucesso! 💬")
                    st.markdown(f"**Comentário gerado:** {comentario}")
                    if acao == "curtir_comentar_compartilhar":
                        st.info("📣 Como é um post da MJV, a RANA também vai compartilhar.")
                else:
                    st.error("Erro ao enviar para o Make")
                    st.text(response.text)
        else:
            st.warning("Preencha o URN e o conteúdo do post.")
