from openai import OpenAI
from services.google_sheets import obter_conteudo_salvo, obter_ultimas_interacoes
from services.web_search import buscar_web
from services.openrouter_api import responder_pergunta
from services.google_sheets import conectar_sheets
import streamlit as st
import json

client = OpenAI(
    api_key=st.secrets["OPENROUTER_API_KEY"],
    base_url="https://openrouter.ai/api/v1",
    default_headers={
        "HTTP-Referer": "https://openrouter.ai",
        "X-Title": "RANA Assistant"
    }
)

def interpretar_comando_geral(comando):
    prompt = f"""
Você é uma assistente pessoal chamada RANA.

O usuário vai falar comandos de voz como:
- "me ajude a criar um relatório de visitas"
- "qual foi a performance do site em março?"
- "quantos leads vieram do Instagram?"
- ou até "me conta uma curiosidade sobre IA"

Sua função é:
1. Interpretar o pedido
2. Se possível, gerar uma resposta ou instrução clara
3. Se não souber como ajudar, diga isso com gentileza.

Comando: "{comando}"
"""
    response = client.chat.completions.create(
        model="openai/gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Você é uma assistente que entende e executa comandos humanos."},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content.strip()


def interpretar_criacao_de_reuniao(comando):
    prompt = f"""
Você é uma assistente chamada RANA que agenda reuniões no Google Calendar.

Interprete o comando abaixo e retorne um dicionário com os campos:
- titulo
- data (formato: AAAA-MM-DD)
- hora_inicio (formato: HH:MM)
- hora_fim (formato: HH:MM)
- convidados (lista de emails, se houver)

Comando do usuário: "{comando}"
Responda apenas com o dicionário JSON, sem explicações.
"""
    response = client.chat.completions.create(
        model="openai/gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Você é uma IA que entende e executa agendamentos de reuniões."},
            {"role": "user", "content": prompt}
        ]
    )
    try:
        return json.loads(response.choices[0].message.content.strip())
    except Exception:
        return None


def resumir_resultados_web(resultados):

    conteudo = "\n\n".join([f"{r['title']} — {r['body']}" for r in resultados])

    prompt = f"""
Você é uma IA pesquisadora que prioriza dados de fontes oficiais, confiáveis e relevantes.

Com base nos resultados de busca abaixo, gere um resumo claro e objetivo sobre o tema.

Dê preferência a conteúdos vindos de domínios .gov, .org, .edu ou veículos de imprensa reconhecidos.

Conteúdo encontrado:
{conteudo}
"""

    response = client.chat.completions.create(
        model="openai/gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Você resume informações com clareza e precisão."},
            {"role": "user", "content": prompt}
        ]
    )

    return response.choices[0].message.content.strip()

def responder_pergunta(pergunta, contexto):
    prompt = f"""Com base nas informações a seguir, responda a pergunta de forma clara e objetiva.
Contexto:
{contexto}

Pergunta: {pergunta}
"""
    response = openai.ChatCompletion.create(
        model="openai/gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Você é uma assistente especializada em Web Analytics e CRM HubSpot."},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content.strip()

def responder_com_contexto(pergunta):
    # Coletando dados do Google Sheets
    from services.google_sheets import conectar_sheets

    base_data, arquivos_data, historico_data, websubmit_data = conectar_sheets()
    
    # Montar contexto com os dados das 4 páginas
    contexto = ""
    contexto += "\nBase Data:\n" + "\n".join([str(d) for d in base_data])  # Transformar dados em string
    contexto += "\nArquivos Data:\n" + "\n".join([str(d) for d in arquivos_data])
    contexto += "\nHistorico Data:\n" + "\n".join([str(d) for d in historico_data])
    contexto += "\nWebSubmit Data:\n" + "\n".join([str(d) for d in websubmit_data])

    # Enviar a pergunta e contexto para o OpenRouter
    resposta = responder_pergunta(pergunta, contexto)
    
    return resposta