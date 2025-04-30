from openai import ChatCompletion

def gerar_post_redes_sociais(comando):
    prompt = f"""
Você é uma assistente de marketing de conteúdo especializada em redes sociais.

Com base no comando abaixo, gere um post completo com:
- Texto principal (em tom leve e profissional)
- Lista de hashtags relevantes
- Sugestão de imagem ou ideia visual
- Dica de horário ideal de postagem

Comando do usuário: "{comando}"
Responda no formato:

Post:
[texto]

Hashtags:
[#hashtag1 #hashtag2 ...]

Visual sugerido:
[descrição clara e detalhada da imagem que represente bem o conteúdo]

Melhor horário de postagem:
[horário ideal]
"""

    resposta = ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Você cria posts criativos e objetivos para redes sociais."},
            {"role": "user", "content": prompt}
        ]
    )

    return resposta.choices[0].message.content.strip()
