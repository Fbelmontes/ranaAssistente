import requests
import streamlit as st

OPENROUTER_KEY = st.secrets["OPENROUTER_API_KEY"]

def gerar_post_blog(pergunta, resposta):
    prompt = f"""
Com base na seguinte resposta técnica gerada a partir de materiais aprendidos:

\"\"\"{resposta}\"\"\"

E considerando a pergunta original:
\"{pergunta}\"

Gere um conteúdo para blog seguindo este formato:
- Um título criativo e objetivo
- Uma introdução curta que gere empatia e conexão
- Subtópicos claros (use H2 e H3)
- Conclusão com um CTA (chamada para ação)
- Linguagem humana, leve, mas profissional
- Se possível, adicione emojis e exemplos reais

Resposta:
"""

    headers = {
        "Authorization": f"Bearer {OPENROUTER_KEY}",
        "Content-Type": "application/json"
    }

    body = {
        "model": "gpt-3.5-turbo",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.8
    }

    response = requests.post("https://openrouter.ai/api/v1/chat/completions", json=body, headers=headers)

    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"]
    else:
        st.error(f"Erro ao gerar post: {response.status_code}")
        st.text(response.text)
        return "Erro ao gerar conteúdo."
