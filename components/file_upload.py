import streamlit as st
from services.file_reader import read_file
from services.google_sheets import salvar_na_memoria  # ajuste conforme seu método


def file_upload_component():
    st.subheader("📂 Enviar Arquivo para Aprendizado da RANA")
    uploaded_file = st.file_uploader("Escolha um arquivo", type=["pdf", "docx", "txt", "csv"])

    if uploaded_file is not None:
        with open(uploaded_file.name, "wb") as f:
            f.write(uploaded_file.getbuffer())

        conteudo = read_file(uploaded_file.name)

        st.success("Arquivo lido com sucesso!")
        st.text_area("Conteúdo do Arquivo:", conteudo[:3000], height=300)  # Mostra só uma parte

        if st.button("Salvar na Memória da RANA"):
            resultado = salvar_na_memoria(conteudo, uploaded_file.name)  # você pode adaptar isso
            st.success("Conteúdo salvo na memória da RANA!" if resultado else "Erro ao salvar")
