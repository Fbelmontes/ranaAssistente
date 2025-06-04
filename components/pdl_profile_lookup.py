import streamlit as st
from services.pdl_api import buscar_perfil_pdl

def mostrar_dado(label, valor):
    if valor:
        st.write(f"{label} {valor}")
    else:
        st.write(f"{label} _não encontrado_ ❌")

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

                # Verifica se o perfil tem dados úteis
                dados_principais = [
                    resultado.get("full_name"),
                    resultado.get("job_title"),
                    resultado.get("job_company_name"),
                    resultado.get("linkedin_url")
                ]

                if not any(dados_principais):
                    st.warning("⚠️ Perfil encontrado, mas sem dados relevantes disponíveis.")

                # Mostra os campos com fallback elegante
                mostrar_dado("👤 Nome:", resultado.get("full_name"))
                mostrar_dado("💼 Cargo:", resultado.get("job_title"))
                mostrar_dado("🏢 Empresa:", resultado.get("job_company_name"))
                mostrar_dado("📍 Localização:", resultado.get("location_city"))
                mostrar_dado("🔗 LinkedIn:", resultado.get("linkedin_url"))
                mostrar_dado("🎯 Interesses:", resultado.get("interests"))

                # Espaço para evoluir com nova tentativa
                st.markdown("---")
                if st.button("🔁 Tentar com outra abordagem (ex: nome + empresa apenas)"):
                    st.info("🚧 Essa funcionalidade ainda está em construção.")

        else:
            st.warning("⚠️ Por favor, preencha o nome.")
