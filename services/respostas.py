import json
from services.memoria import ler_toda_memoria
from services.openrouter_api import responder_pergunta

def responder_com_contexto(pergunta):
    memoria = ler_toda_memoria()
    base_conhecimento = json.dumps(memoria, ensure_ascii=False)

    prompt = f"""
Você é a RANA, uma assistente com acesso a dados sobre empresas.

Responda com base nos dados abaixo (não invente nada):

{base_conhecimento}

Pergunta: {pergunta}
Resposta:
"""
    return responder_pergunta(prompt)
