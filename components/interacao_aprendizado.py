import streamlit as st
from services.webscraping import buscar_informacoes
from services.memoria import salvar_aprendizado, recuperar_aprendizado

def interacao_aprendizado():
    st.subheader("📚 Aprender sobre uma empresa")
    termo = st.text_input("Digite o nome da empresa ou site:")

    if st.button("Buscar e Aprender"):
        with st.spinner("Buscando e aprendendo..."):
            dados = buscar_informacoes(termo)
            #salvar_aprendizado(termo, dados)
            st.success("Informações aprendidas com sucesso!")
            st.json(dados)

    if st.button("Ver o que a RANA já sabe"):
        contexto = recuperar_aprendizado(termo)
        if contexto:
            st.markdown("### 🧠 Conhecimento aprendido:")
            st.json(contexto)
        else:
            st.info("Nada aprendido ainda sobre esse termo.")
