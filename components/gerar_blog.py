import streamlit as st
from services.gerador_conteudo import gerar_post_blog, gerar_docx, gerar_pdf

def gerar_blog_component():
    st.subheader("📝 Gerar Conteúdo para Blog com base em uma Resposta")

    pergunta = st.text_input("Qual foi a pergunta feita para a RANA?")
    resposta = st.text_area("Cole aqui a resposta que a RANA deu:", height=300)

    if st.button("Gerar Conteúdo de Blog"):
        with st.spinner("RANA está gerando o conteúdo..."):
            post = gerar_post_blog(pergunta, resposta)
            st.markdown("### Conteúdo gerado:")
            st.markdown(post)
           
             # Gerar DOCX e PDF e garantir que o conteúdo seja retornado corretamente
            docx_path = gerar_docx(post)
            st.download_button("Baixar como DOCX", docx_path, file_name="conteudo_blog.docx")

            pdf_path = gerar_pdf(post)
            st.download_button("Baixar como PDF", pdf_path, file_name="conteudo_blog.pdf")