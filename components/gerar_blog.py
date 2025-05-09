import streamlit as st
from services.gerador_conteudo import gerar_post_blog, buscar_criticas_newsapi, gerar_docx, gerar_pdf

def gerar_blog_component():
    st.subheader("📝 Gerar Conteúdo para Blog com base em uma Resposta")

    pergunta = st.text_input("Qual foi a pergunta feita para a RANA?")
    resposta = st.text_area("Cole aqui a resposta que a RANA deu:", height=300)
    tema = st.text_input("Digite o tema para buscar críticas e artigos:")

    if st.button("Gerar Conteúdo de Blog"):
        with st.spinner("RANA está gerando o conteúdo..."):
            post = gerar_post_blog(pergunta, resposta)
            st.markdown("### Conteúdo gerado:")
            st.markdown(post)

            # Buscar críticas/artigos relacionados ao tema
            if tema:
                criticas = buscar_criticas_newsapi(tema)
                if not criticas:
                    st.write("Nenhuma crítica encontrada na NewsAPI.")
                
            # Gerar DOCX e PDF para o conteúdo ajustado
            docx_file = gerar_docx(post_ajustado)
            st.download_button("Baixar como DOCX", docx_file, file_name="conteudo_blog.docx", mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document")

            pdf_file = gerar_pdf(post_ajustado)
            st.download_button("Baixar como PDF", pdf_file, file_name="conteudo_blog.pdf", mime="application/pdf")
