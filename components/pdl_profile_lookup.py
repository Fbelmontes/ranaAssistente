import streamlit as st
from services.pdl_api import buscar_perfil_pdl

def mostrar_dado(label, valor):
    if valor:
        st.write(f"{label} {valor}")
    else:
        st.write(f"{label} _não encontrado_ ❌")

def pdl_profile_lookup_component():
    st.subheader("🔎 Busca Inteligente de Perfis com PDL")

    nome = st.text_input("Nome completo (opcional)")
    email = st.text_input("E-mail (opcional)")

    if st.button("🔍 Buscar Perfis"):
        resultado = buscar_perfis_pdl(nome, email)

        if "erro" in resultado:
            st.error(resultado["erro"])
        elif not resultado.get("data"):
            st.warning("😕 Nenhum perfil encontrado.")
        else:
            st.success("✅ Perfis encontrados:")

            for i, perfil in enumerate(resultado["data"][:3]):
                with st.container():
                    st.markdown(f"**{perfil.get('full_name', 'Sem nome')}**")
                    st.write("💼", perfil.get("job_title", "Cargo não disponível"))
                    st.write("🏢", perfil.get("job_company_name", "Empresa não disponível"))
                    st.write("📍", perfil.get("location", "Localização não disponível"))
                    linkedin = perfil.get("linkedin_url")
                    if linkedin:
                        st.markdown(f"[🔗 Ver LinkedIn]({linkedin})", unsafe_allow_html=True)

                    if st.button(f"✅ Usar este perfil ({i+1})"):
                        st.info(f"📌 Perfil selecionado: {perfil.get('full_name')} - {linkedin or 'sem link'}")