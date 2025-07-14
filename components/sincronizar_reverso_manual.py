
import streamlit as st
from services.sincronizar_reverso import buscar_negocios_tap, sincronizar_para_origem

def sincronizar_reverso_manual_component():
    st.subheader("🔄 Atualizar valores no negócio de origem")

    if st.button("Executar sincronização agora"):
        with st.spinner("Buscando negócios na TAP & Kickoff..."):
            negocios = buscar_negocios_tap()

        if not negocios:
            st.info("Nenhum negócio com deal_id_origem encontrado.")
            return

        resultados = []
        with st.spinner("Sincronizando com negócios de origem..."):
            for negocio in negocios:
                resultado = sincronizar_para_origem(negocio)
                resultados.append(resultado)

        st.success("Sincronização finalizada.")
        for res in resultados:
            st.markdown(res)
