import streamlit as st
import base64
import pandas as pd
import json

# Chamadas de arquivos 
from services.webscraping import buscar_informacoes
from services.google_sheets import salvar_na_planilha_2, conectar_sheets
from components.enviar_evento_make import enviar_evento_make_component

# Configuração da página
st.set_page_config(page_title="RANA - Assistente", page_icon="🤖", layout="wide")

if "tema_escuro" not in st.session_state:
    st.session_state.tema_escuro = False

# Funções para converter imagens e vídeos
def image_to_base64(path):
    with open(path, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

def video_to_base64(path):
    with open(path, "rb") as video_file:
        video_bytes = video_file.read()
    return base64.b64encode(video_bytes).decode()

# Base64 do vídeo
video_base64 = video_to_base64("assets/videos/rana_avatar.mp4")

# Título da aplicação
col_logo, col_titulo = st.columns([1, 6])

with col_titulo:
    st.markdown(
        """
        <h1 style='color:#003366; line-height: 60px; display: flex; align-items: center;'>
            <img src='data:image/png;base64,{img_base64}' width='60' style='margin-right: 10px;'/>
            RANA - Assistente de Web Analytics
        </h1>
        """.format(img_base64=image_to_base64("assets/icons/style_rana.png")),
        unsafe_allow_html=True
    )

st.caption("Powered by você, Fe 💖")

# Layout: Menu | Avatar | Interação
col_menu, col_avatar, col_content = st.columns([1, 1, 2])

# ========== MENU LADO ESQUERDO ==========

# Usando a barra lateral para menu
with st.sidebar:
    st.markdown("## 🧭 Menu", unsafe_allow_html=True)

    # Categorias de Menu
    menu_opcoes = {
        "🔍 Pesquisa": [
            "🔍 Buscar Empresa ou Site",
            "📚 Aprender sobre um site",
            "🌐 Pesquisar na Web"
        ],
        "⚙️ Automação de Marketing": [
            "📅 Criar Evento de Marketing",
            "📤 Importar Leads",
            "💬 Curtir e comentar post"
        ],
        "📚 Aprendizado / 🤖 Memória": [
            "📚 Enviar Material para Aprendizado",
            "🤖 Perguntar com base nos Aprendizados",
            "📝 Gerar Conteúdo para Blog"
        ],
        "🌍 Web Scraping": [
            "🌍 Web Scraping Web Summit"
        ],
        "🛡️ Autenticação HubSpot": [
            "🔐 Gerar Token de Acesso",
            "🔄 Renovar Token de Acesso"
        ]
    }

    # Menu com categorias
    categoria = st.radio("Escolha uma categoria", list(menu_opcoes.keys()))

    # Opções dentro da categoria selecionada
    escolha = st.radio("Escolha uma opção", menu_opcoes[categoria], index=0)

# ========== AVATAR CENTRAL ==========

with col_avatar:
    st.markdown(
        f"""
        <div style="
            background: rgba(255, 255, 255, 0.6);
            border: 2px solid #ccc;
            border-radius: 20px;
            padding: 20px;
            text-align: center;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
        ">
            <video width="400" autoplay loop muted playsinline style="border-radius: 40px;" >
                <source src="data:video/mp4;base64,{video_base64}" type="video/mp4">
                Seu navegador não suporta vídeo incorporado 😢
            </video>
        </div>
        """,
        unsafe_allow_html=True
    )

# ========== CONTEÚDO À DIREITA ==========

with col_content:
    st.markdown("### Área de Interação")

    # ############# Opção MENU #############
    if escolha == "🌍 Web Scraping Web Summit":
        st.subheader("🕵️‍♂️ Coletando Palestras e Eventos do Web Summit")
        
        progress_var = st.progress(0)  # Barra de progresso para feedback ao usuário

        if st.button("Coletar Dados do Web Summit"):
            with st.spinner("Coletando dados..."):
                eventos = start_scraping()  # Função de scraping
                
                if eventos is not None:
                    df = eventos
                    st.dataframe(df)  # Exibe os dados no formato de tabela
                    st.success("Dados coletados com sucesso!")
                    
                    # Optionally, save to Google Sheets (if needed)
                    #salvar_historico("Web Summit - Eventos", df.to_dict(orient='records'))
                else:
                    st.error("Erro ao coletar dados.")

    elif escolha == "📚 Aprender sobre um site":
        st.subheader("Ensinar algo novo para a RANA")
        url = st.text_input("Insira o link do site:")
        if st.button("Aprender"):
            with st.spinner("Lendo e aprendendo com o site..."):
                conteudo = extrair_texto(url)
                if "Erro" in conteudo:
                    st.error(conteudo)
                else:
                    salvar_na_planilha(url, conteudo)
                    st.success("Aprendizado completo! 🎓")
                    st.text_area("Resumo do Conteúdo:", conteudo, height=200)
    
    elif escolha == "🌐 Pesquisar na Web":
        st.subheader("Pesquisa com RANA na internet")

        tema = st.text_input("Sobre o que você quer saber?")
        if st.button("Pesquisar e Resumir"):
            from services.web_search import buscar_web
            from services.openrouter_api import resumir_resultados_web

            with st.spinner("RANA está pesquisando..."):
                resultados = buscar_web(tema)
                resumo = resumir_resultados_web(resultados)

                st.success("Resumo encontrado:")
                st.markdown(resumo)

                salvar_historico(f"Pesquisa na web: {tema}", resumo)

                st.markdown("### Fontes:")
                for r in resultados:
                    st.markdown(f"- [{r['title']}]({r['href']})")

    elif escolha == "📤 Importar Leads":
        from components.csv_upload import upload_leads_para_evento
        upload_leads_para_evento()

    elif escolha == "🤖 Fazer uma pergunta":
        from services.respostas import responder_com_contexto

        st.subheader("Pergunte algo com base na memória da RANA")
        pergunta = st.text_input("Digite sua pergunta:")

        if st.button("Perguntar"):
            with st.spinner("RANA está pensando..."):
                resposta = responder_com_contexto(pergunta)
                if resposta:
                    st.success("Resposta da RANA:")
                    st.markdown(f"**RANA:** {resposta}")
                else:
                    st.error("Desculpe, não consegui encontrar nada.")

    elif escolha == "🔍 Buscar Empresa ou Site":
        from components.interacao_aprendizado import interacao_aprendizado
        interacao_aprendizado()
    
    elif escolha == "💬 Curtir e comentar post":
        from components.linkedin_interact import linkedin_interaction_component
        linkedin_interaction_component()

    elif escolha == "📚 Enviar Material para Aprendizado":
        from components.upload_material import upload_material_component
        upload_material_component()
        from services.openrouter_api import listar_modelos_disponiveis

    elif escolha == "🤖 Perguntar com base nos Aprendizados":
        from components.perguntas_aprendizado import perguntas_aprendizado_component
        perguntas_aprendizado_component()

    elif escolha == "📝 Gerar Conteúdo para Blog":
        from components.gerar_blog import gerar_blog_component
        gerar_blog_component()
       
    elif escolha == "📅 Criar Evento de Marketing":
        from components.criar_evento import criar_evento_component
        criar_evento_component()
    
    elif escolha == "🔄 Renovar Token de Acesso":
        from components.renovar_token import renovar_token_component
        renovar_token_component()

    elif escolha == "🔐 Gerar Token de Acesso":
        from components.gerar_token import gerar_token_component
        gerar_token_component()