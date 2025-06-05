import streamlit as st

def rocketreach_profile_lookup_component():
    st.subheader("🚀 Resultados da Busca de Perfis (Mock)")

    resultados = [
        {
            "nome": "Felipe Silva",
            "cargo": "Technology Vice President",
            "empresa": "Goldman Sachs",
            "localizacao": "London, GB",
            "email": "felipe.silva@gmail.com",
            "empresa_email": "gs.com",
            "linkedin": "https://linkedin.com/in/felipe-silva-goldman",
            "imagem": "https://randomuser.me/api/portraits/men/44.jpg"
        },
        {
            "nome": "Felipe Silva",
            "cargo": "IT Director",
            "empresa": "Grupo Casas Bahia",
            "localizacao": "São Paulo, BR",
            "email": "felipe@yahoo.com.br",
            "empresa_email": "casasbahia.com.br",
            "linkedin": "https://linkedin.com/in/felipe-silva-casasbahia",
            "imagem": "https://randomuser.me/api/portraits/men/88.jpg"
        }
    ]

    for i, perfil in enumerate(resultados):
        with st.container():
            col1, col2 = st.columns([1, 6])
            with col1:
                st.image(perfil["imagem"], width=100)
            with col2:
                st.markdown(f"### {perfil['nome']}")
                st.write("💼", perfil["cargo"])
                st.write("🏢", perfil["empresa"])
                st.write("📍", perfil["localizacao"])
                st.write("📧", perfil["email"], " | 🏢", perfil["empresa_email"])
                st.markdown(f"[🔗 Ver LinkedIn]({perfil['linkedin']})", unsafe_allow_html=True)

                if st.button(f"✅ Usar este perfil {i+1}"):
                    st.success(f"Perfil selecionado: {perfil['nome']} ({perfil['linkedin']})")

            st.markdown("---")
