import streamlit as st
from services.sincronizar_negocios import buscar_negocios_clonados, sincronizar_negocio

def sincronizar_manual_component():
    st.subheader("🔄 Atualizar Negócios Clonados")

    if st.button("Atualizar negócios agora"):
        with st.spinner("Buscando negócios clonados..."):
            negocios = buscar_negocios_clonados()

        if not negocios:
            st.info("Nenhum negócio clonado encontrado com deal_id_origem preenchido.")
            return

        resultados = []
        with st.spinner("Sincronizando com negócios de origem..."):
            for negocio in negocios:
                resultado = sincronizar_negocio(negocio)
                resultados.append(resultado)

        st.success("Sincronização concluída!")
        for res in resultados:
            st.markdown(res)
