import streamlit as st
from services.rocketreach_api import buscar_perfil_rocketreach

def rocketreach_profile_lookup_component():
    st.subheader("🚀 Buscar Perfil com RocketReach")

    nome = st.text_input("Nome completo (opcional)")
    email = st.text_input("E-mail (opcional)")
    empresa = st.text_input("Empresa (obrigatória se buscar por nome)")

    if st.button("🔍 Buscar Perfil"):
        resultado = buscar_perfil_rocketreach(nome, email, empresa)

        if "erro" in resultado:
            st.error(resultado["erro"])
        else:
            st.success("✅ Perfil encontrado!")

            st.write("👤 Nome:", resultado.get("name") or "Não encontrado")
            st.write("💼 Cargo:", resultado.get("current_title") or "Não encontrado")
            st.write("🏢 Empresa:", resultado.get("current_employer") or "Não encontrado")
            st.write("📍 Localização:", resultado.get("location") or "Não disponível")
            linkedin = resultado.get("linkedin_url")
            if linkedin:
                st.markdown(f"[🔗 Ver LinkedIn]({linkedin})", unsafe_allow_html=True)
            else:
                st.write("🔗 LinkedIn: Não disponível")

            if st.button("✅ Usar este perfil"):
                st.info(f"Perfil selecionado: {resultado.get('name')} — {linkedin or 'sem link'}")
