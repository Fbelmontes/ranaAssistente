import streamlit as st
from services.sincronizar_negocios import buscar_negocios_tap, sincronizar_para_origem

def sincronizar_manual_component():
    st.subheader("🔁 Sincronizar negócios da TAP com origem")

    if st.button("🔄 Atualizar negócios de origem"):
        negocios = buscar_negocios_tap()
        if not negocios:
            st.warning("⚠️ Nenhum negócio elegível encontrado.")
        else:
            for negocio in negocios:
                resultado = sincronizar_para_origem(negocio)
                st.write(resultado)
