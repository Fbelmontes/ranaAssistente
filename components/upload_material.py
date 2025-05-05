import streamlit as st
from services.extrair_conteudo import extrair_texto_arquivo
from services.memoria import salvar_aprendizado

def upload_material_component():
    st.subheader("📚 Aprender com Material Enviado")

    uploaded_file = st.file_uploader("Envie um arquivo (PDF, DOCX, TXT)", type=["pdf", "docx", "txt"])

    if uploaded_file:
        nome_material = st.text_input("Dê um título para este material:")

        if st.button("Aprender com o material"):
            with st.spinner("Lendo conteúdo..."):
                texto_extraido = extrair_texto_arquivo(uploaded_file)

                if "Formato não suportado" in texto_extraido:
                    st.error(texto_extraido)
                    return

                salvar_aprendizado(nome_material or uploaded_file.name, texto_extraido)

                st.success("✅ Aprendizado salvo com sucesso!")
                st.markdown("### Prévia do conteúdo aprendido:")
                st.text_area("Texto extraído:", texto_extraido[:2000], height=300)
