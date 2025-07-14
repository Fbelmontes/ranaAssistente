import streamlit as st
from services.sincronizar_negocios import buscar_negocios_tap, sincronizar_para_origem

def sincronizar_reverso_manual_component():
    st.subheader("🔁 Atualizar negócios de origem (Reverso)")

    if st.button("🔄 Atualizar agora"):
        with st.spinner("Sincronizando..."):
            negocios = buscar_negocios_tap()
            if not negocios:
                st.warning("⚠️ Nenhum negócio elegível encontrado.")
                return

            logs = []
            for negocio in negocios:
                resultado = sincronizar_para_origem(negocio)
                logs.append(resultado)

            st.success("✅ Sincronização finalizada")
            for log in logs:
                st.write(log)
