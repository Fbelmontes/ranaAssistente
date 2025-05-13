import streamlit as st

def exibir_relatorio_lookerstudio():
    st.subheader("📊 Relatórios de Tráfego e Comportamento")

    # Inserir o link do Looker Studio
    link_relatorio = st.text_input("https://lookerstudio.google.com/u/0/reporting/ec32de22-89ce-4636-bba1-e7f93e21d84a/page/p_ztgneftsqd?params=%7B%22dp263%22:%22a33651351w322096300%22%7D")
    
    if link_relatorio:
        st.markdown(f"#### Visualização do Relatório")
        st.markdown(f'<iframe src="{link_relatorio}" width="100%" height="600"></iframe>', unsafe_allow_html=True)
