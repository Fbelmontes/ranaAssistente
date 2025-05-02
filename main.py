# Execução python -m streamlit run .\main.py
import streamlit as st
import base64
import pandas as pd
from styles import css_claro, css_escuro
from services.openrouter_api import responder_pergunta
from services.google_sheets import (
    obter_conteudo_salvo,
    salvar_na_planilha,
    salvar_transcricao,
    buscar_na_memoria
)
from services.scraping import extrair_texto
#from services.audio_transcriber import gravar_reuniao, transcrever_reuniao
from services.relatorio_generator import gerar_relatorio
#from components.file_upload import file_upload_component
from services.google_calendar import verificar_eventos, criar_evento
from services.google_sheets import salvar_historico
from services.google_sheets import obter_ultimas_interacoes
from services.image_generator import gerar_imagem
from components.webscraping import start_scraping


st.set_page_config(page_title="RANA - Assistente", page_icon="🤖", layout="wide")

if "tema_escuro" not in st.session_state:
    st.session_state.tema_escuro = False

# imagem para GIF
def image_to_base64(path):
    with open(path, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

# imagem para video
def video_to_base64(path):
    with open(path, "rb") as video_file:
        video_bytes = video_file.read()
    return base64.b64encode(video_bytes).decode()

video_base64 = video_to_base64("assets/videos/rana_avatar.mp4")

#gif_base64 = image_to_base64("assets/icons/rana_avatar2.gif")

st.markdown(css_escuro if st.session_state.tema_escuro else css_claro, unsafe_allow_html=True)

#st.markdown("<h1 style='color:#003366; text-align: center;'> RANA - Assistente de Web Analytics</h1>", unsafe_allow_html=True)
#st.caption("Powered by você, Fe 💖")
col_logo, col_titulo = st.columns([1, 6])

with col_titulo:
    st.markdown(
        """
        <h1 style='color:#003366; line-height: 60px; display: flex; align-items: center;'>
            <img src='data:image/png;base64,{img_base64}' width='120' style='margin-right: 10px;'/>
            RANA - Assistente de Web Analytics
        </h1>
        """.format(img_base64=image_to_base64("assets/icons/style_rana.png")),
        unsafe_allow_html=True
    )


st.caption("Powered by você, Fe 💖")


# Layout: Menu | Avatar | Interação
col_menu, col_avatar, col_content = st.columns([1, 1, 2])

# ========== MENU LADO ESQUERDO ==========
with col_menu:
    st.markdown("## 🧭 Menu", unsafe_allow_html=True)
    escolha = st.radio(
        "",
        ["📚 Aprender sobre um site","🌐 Pesquisar na Web","📤 Importar Leads","🌍 Web Scraping Web Summit","🤖 Fazer uma pergunta"], #,"📁 Enviar Arquivo","🗣️ Falar com a RANA", "🤖 Fazer uma pergunta","📆 Google Calendar", "🎤 Observar Reunião","📲 Criar post para redes", "🎨 Alternar tema"],
        index=1
    )

# ========== AVATAR CENTRAL ==========
with col_avatar:
    #st.image("assets/icons/rana_avatar.gif", width=240)
    #st.video("assets/videos/rana_avatar.mp4")
    #st.markdown("<p style='text-align:center; color:#666;'>RANA em operação...</p>", unsafe_allow_html=True)
    # Insere HTML + JavaScript no Streamlit
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
        <p style='color:#003366; font-weight: 500; margin-top: 10px;'></p>
    </div>
    """,
    unsafe_allow_html=True
)

# ========== CONTEÚDO À DIREITA ==========
with col_content:
    st.markdown("### Área de Interação")

    # ############# Opção Web Scraping #############
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
        from components.csv_upload import upload_csv_para_make
        upload_csv_para_make()

    elif escolha == "🗣️ Falar com a RANA":
        st.subheader("Comando por voz")

        if st.button("Falar agora"):
            from services.audio_input import capturar_comando_voz
            from services.audio_transcriber import transcrever_reuniao
            from services.openrouter_api import interpretar_criacao_de_reuniao
            from services.google_calendar import criar_evento
            import datetime

            with st.spinner("RANA está ouvindo..."):
                audio_path = capturar_comando_voz()
                texto = transcrever_reuniao(audio_path)
                st.markdown(f"**Você disse:** {texto}")

                info = interpretar_criacao_de_reuniao(texto)

                if not info:
                    st.warning("Desculpe, não consegui entender seu pedido.")
                else:
                    st.json(info)  # opcional: mostrar o que foi interpretado

                    try:
                        dt_inicio = datetime.datetime.fromisoformat(f"{info['data']}T{info['hora_inicio']}")
                        dt_fim = datetime.datetime.fromisoformat(f"{info['data']}T{info['hora_fim']}")
                        convidados = info.get("convidados", [])

                        link = criar_evento(info['titulo'], dt_inicio.isoformat(), dt_fim.isoformat(), convidados)
                        st.success(f"Reunião criada com sucesso! [Acessar evento]({link})")
                    except Exception as e:
                        st.error(f"Erro ao criar reunião: {e}")



    elif escolha == "📁 Enviar Arquivo":
        st.subheader("Enviar Arquivo para a RANA Aprender 📂")
        file_upload_component()

    elif escolha == "🤖 Fazer uma pergunta":
        st.subheader("Fazer uma pergunta para a RANA")
        pergunta = st.text_input("Digite sua pergunta:")

        if st.button("Perguntar"):
            with st.spinner("RANA está pensando..."):
                 # 🔁 Dados principais (base de aprendizado)
                dados = obter_conteudo_salvo()
                contexto_dados = "\n".join([
                    f"URL: {d.get('URL', '')}\nConteúdo: {d.get('Conteudo', '')}" for d in dados
                ])

                # 🧠 Histórico recente (memória curta)
                historico = obter_ultimas_interacoes()
                memoria = "\n".join([
                    f"Pergunta: {h['Pergunta']}\nResposta: {h['Resposta']}" for h in historico
                ])

                # 🧬 Contexto total: memória + base de dados
                contexto = f"{memoria}\n\n{contexto_dados}"

                # 🤖 Chamada para responder
                resposta = responder_pergunta(pergunta, contexto)
                st.success("Resposta da RANA:")
                st.markdown(f"**RANA:** {resposta}")

                salvar_historico(pergunta, resposta)


    elif escolha == "🔍 Buscar Aprendizado":
        st.subheader("🔎 Buscar por Palavra-chave nos Aprendizados")
        palavra_chave = st.text_input("Digite a palavra-chave que deseja buscar:")

        if st.button("Buscar"):
            with st.spinner("Procurando nos aprendizados..."):
                resultados = buscar_na_memoria(palavra_chave)
                if resultados:
                    st.success("Resultados encontrados:")
                    for resultado in resultados:
                        st.markdown(f"**Arquivo:** {resultado['Nome do Arquivo']}")
                        st.text_area(f"Conteúdo:", resultado['Conteúdo'], height=150)
                    else:
                        st.warning("Nenhum resultado encontrado para essa palavra-chave.")

    elif escolha == "📆 Google Calendar":

        if st.button("Verificar eventos"):
            eventos = verificar_eventos()
            for e in eventos:
                st.markdown(f"- {e}")

            st.subheader("Criar novo evento no Google Calendar")

        titulo = st.text_input("Título da reunião:", "Reunião com RANA")
        data_evento = st.date_input("Data do evento")
        hora_inicio = st.time_input("Horário de início")
        hora_fim = st.time_input("Horário de término")

        convidados_raw = st.text_input("E-mails dos convidados (separados por vírgula)", "exemplo@email.com")

        if st.button("Criar evento"):
            from services.google_calendar import criar_evento
            import datetime

            dt_inicio = datetime.datetime.combine(data_evento, hora_inicio)
            dt_fim = datetime.datetime.combine(data_evento, hora_fim)
            convidados = [email.strip() for email in convidados_raw.split(",") if email.strip()]

            link = criar_evento(titulo, dt_inicio.isoformat(), dt_fim.isoformat(), convidados)
            st.success(link)


    elif escolha == "🎤 Observar Reunião":
        st.subheader("Observar e Aprender com a Reunião")
        duracao = st.slider("Duração da gravação (segundos)", 5, 60, 10)
        if st.button("Iniciar Gravação"):
            with st.spinner("Gravando e transcrevendo..."):
                audio_path = gravar_reuniao(duracao)
                texto = transcrever_reuniao(audio_path)
                salvar_transcricao(texto)
                st.success("Transcrição salva com sucesso! 📝")
                st.text_area("Transcrição da Reunião:", texto, height=200)

    elif escolha == "📲 Criar post para redes":
        st.subheader("Criação de conteúdo para redes sociais")

        briefing = st.text_area("Descreva o conteúdo que você quer postar (tema, evento, produto, etc):")

        if st.button("Gerar conteúdo"):
            from services.social_creator import gerar_post_redes_sociais
            from services.image_generator import gerar_imagem
            from services.google_sheets import salvar_historico
            import re

            with st.spinner("Criando post..."):
                resposta = gerar_post_redes_sociais(briefing)
                st.success("Post gerado com sucesso!")

                st.markdown(resposta)
                salvar_historico(f"Post para redes: {briefing}", resposta)

                # Extrair descrição visual do texto
                padrao = r"Visual sugerido:\s*(.*)"
                match = re.search(padrao, resposta)

                if match and match.group(1).strip():
                    prompt_visual = match.group(1).strip()
                    url = gerar_imagem(prompt_visual)
                    if url:
                        st.image(url, caption="Imagem sugerida pela RANA")
                    else:
                        st.warning("Não foi possível gerar a imagem com esse prompt.")
                else:
                    st.info("Nenhuma descrição visual foi encontrada no conteúdo gerado.")



    elif escolha == "🎨 Alternar tema":
        st.session_state.tema_escuro = not st.session_state.tema_escuro
        st.experimental_rerun()
