import streamlit as st
import base64
import pandas as pd
import json

# Chamadas de arquivos 
from services.webscraping import buscar_informacoes, scraping_evento_component
from services.google_sheets import salvar_na_planilha_2, conectar_sheets
from components.enviar_evento_make import enviar_evento_make_component
from components.linkedin_integration import linkedin_integration_component
from components.consultar_eventos import consultar_eventos_component
from components.trello_sync_component import trello_sync_component
from services.verificar_leads_hubspot import buscar_leads_na_base
from components.rocketreach_profile_lookup import rocketreach_profile_lookup_component
from components.url_input import url_input_component #WebHook N8N

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
            <img src='data:image/png;base64,{img_base64}' style='max-width: 100px; height: auto; margin-right: 10px;'/>
            RANA - Assistente de Web Analytics
        </h1>
        """.format(img_base64=image_to_base64("assets/icons/style_rana.png")),
        unsafe_allow_html=True
    )

st.caption("Powered by você, Fe 💖")

# Layout principal com responsividade otimizada
col_avatar, col_content = st.columns([1, 3])

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
            <video style="max-width: 100%; height: auto; border-radius: 40px;" autoplay loop muted playsinline>
                <source src="data:video/mp4;base64,{video_base64}" type="video/mp4">
                Seu navegador não suporta vídeo incorporado 😞
            </video>
        </div>
        """,
        unsafe_allow_html=True
    )

# ========== MENU LATERAL ==========
with st.sidebar:
    st.markdown("## 🧭 Menu", unsafe_allow_html=True)

    menu_opcoes = {
        "🔍 Pesquisa": [
            "🔍 Buscar Empresa ou Site",
            "📚 Aprender sobre um site",
            "🌐 Pesquisar na Web",
            "📚 Aprender sobre alguem"
        ],
        "⚙️ Automação de Marketing": [
            "📅 Criar Evento de Marketing",
            "📤 Importar Leads",
            #"🔎 Verificar Leads no HubSpot",
            #"💬 Curtir e comentar post",
            #"📅 Consultar Eventos e Participantes LinkedIn",
            "✅ Atualizar Tarefas no Trello",
            "🔄 Atualizar Negócios Clonados"
        ],
        "📚 Aprendizado / 🤖 Memória": [
            #"📚 Enviar Material para Aprendizado",
            #"🤖 Perguntar com base nos Aprendizados",
            #"📝 Gerar Conteúdo para Blog",
            "🤖 Conteudo / Perguntas"
        ],
        "🌍 Web Scraping": [
            "🌍 Web Scraping Web Summit",
            "🌍 Web Scraping Linkedin"
        ],
        "🛡️ Autenticação HubSpot": [
            "🔐 Gerar Token de Acesso",
            "🔄 Renovar Token de Acesso",
            "🔗 Integração com LinkedIn"
        ],
        "📊 Analise":[
            "📊 Relatórios de Tráfego e Comportamento"
        ]
    }

    categoria = st.radio("Escolha uma categoria", list(menu_opcoes.keys()))
    escolha = st.radio("Escolha uma opção", menu_opcoes[categoria], index=0)

# ========== CONTEÚDO À DIREITA ==========
with col_content:
    st.markdown("### Área de Interação")

    if escolha == "🌍 Web Scraping Web Summit":
        st.subheader("🕵️‍♂️ Coletando Palestras e Eventos do Web Summit")
        progress_var = st.progress(0)
        if st.button("Coletar Dados do Web Summit"):
            with st.spinner("Coletando dados..."):
                eventos = start_scraping()
                if eventos is not None:
                    st.dataframe(eventos)
                    st.success("Dados coletados com sucesso!")
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

    elif escolha == "🌍 Web Scraping Linkedin":
        scraping_evento_component()
    
    elif escolha == "🔗 Integração com LinkedIn":
        from components.linkedin_auth import linkedin_auth_component
        linkedin_auth_component()
    
    elif escolha == "📅 Consultar Eventos e Participantes LinkedIn":
        consultar_eventos_component()
    
    elif escolha == "✅ Atualizar Tarefas no Trello":
        trello_sync_component()
    
    elif escolha == "🔎 Verificar Leads no HubSpot":
        
        def verificar_leads_component():
            st.subheader("🔎 Verificar Leads no HubSpot")

            if st.button("🔍 Iniciar verificação"):
                st.info("Pesquisando leads na base do HubSpot...")
                buscar_leads_na_base()
                st.success("Verificação concluída! Resultados atualizados na planilha.")

        verificar_leads_component()
    
    elif escolha == "📚 Aprender sobre alguem":
        rocketreach_profile_lookup_component()
    
    elif escolha == "🤖 Conteudo / Perguntas":
        url_input_component()

    elif escolha == "🔄 Atualizar Negócios Clonados":
        from components.sincronizar_manual import sincronizar_manual_component
        sincronizar_manual_component()   