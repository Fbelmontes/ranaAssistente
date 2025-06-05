import streamlit as st
from services.rocketreach_api import buscar_perfil_rocketreach

def rocketreach_profile_lookup_component():
    st.subheader("🚀 Buscar Perfil via RocketReach")

    nome = st.text_input("Digite o nome completo da pessoa (opcional)")
    email = st.text_input("Digite o e-mail da pessoa (opcional)")

    if st.button("🔍 Buscar Perfil"):
        with st.spinner("Consultando RocketReach..."):
            data, erro = buscar_perfil_rocketreach(nome=nome if nome else None, email=email if email else None)

            if erro:
                st.error(erro)
                return

            if not data:
                st.warning("Nenhum perfil encontrado.")
                return

            st.success("✅ Perfil encontrado!")

            # Tratamento seguro
            nome = data.get("name") or "Não disponível"
            cargo = data.get("current_title") or "Não disponível"
            empresa = data.get("current_employer") or "Não disponível"
            local = data.get("location") or "Não disponível"
            linkedin = data.get("linkedin_url") or "Não disponível"
            imagem = data.get("img") or "https://via.placeholder.com/100"

            col1, col2 = st.columns([1, 6])
            with col1:
                st.image(imagem, width=100)
            with col2:
                st.markdown(f"### {nome}")
                st.write("💼", cargo)
                st.write("🏢", empresa)
                st.write("📍", local)
                st.markdown(f"[🔗 Ver LinkedIn]({linkedin})", unsafe_allow_html=True)

                if st.button("✅ Usar este perfil"):
                    st.success(f"Perfil selecionado: {nome} ({linkedin})")
