import streamlit as st
from services.pdl_api import buscar_perfil_pdl

def pdl_profile_lookup_component():
    st.subheader("🔍 Buscar Perfil com People Data Labs")

    nome = st.text_input("Nome completo")
    email = st.text_input("Email (opcional)")
    empresa = st.text_input("Empresa (opcional)")

    if st.button("Buscar Perfil"):
        if nome:
            resultado = buscar_perfil_pdl(nome, email, empresa)

            if "erro" in resultado:
                st.error(f"❌ {resultado['erro']}")
            else:
                st.success("✅ Perfil encontrado!")
                st.write("👤 Nome:", resultado.get("full_name"))
                st.write("💼 Cargo:", resultado.get("job_title"))
                st.write("🏢 Empresa:", resultado.get("job_company_name"))
                st.write("📍 Localização:", resultado.get("location_city"))
                st.write("🔗 LinkedIn:", resultado.get("linkedin_url"))
                st.write("🎯 Interesses:", resultado.get("interests"))
        else:
            st.warning("⚠️ Por favor, preencha o nome.")
