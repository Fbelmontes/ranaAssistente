import streamlit as st
from services.respostas import responder_com_contexto

def perguntas_aprendizado_component():
    st.subheader("🧠 Pergunte com base nos materiais aprendidos")

    pergunta = st.text_input("Faça sua pergunta:")

    if st.button("Responder"):
        with st.spinner("RANA está consultando o conhecimento..."):
            resposta = responder_com_contexto(pergunta)

        st.markdown("### Resposta da RANA:")
        st.markdown(resposta)