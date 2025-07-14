
import requests
from .hubspot_oauth import renovar_token_automaticamente

CAMPOS_REVERSO = [
    "valor_faturado_ano_atual",
    "valor_faturado_proximos_anos"
]

def buscar_negocios_tap():
    token = renovar_token_automaticamente()
    headers = {
        "Authorization": f"Bearer {token}"
    }

    url = "https://api.hubapi.com/crm/v3/objects/deals"
    params = {
        "limit": 100,
        "properties": f"id_de_origem,{','.join(CAMPOS_REVERSO)}"
    }

    response = requests.get(url, headers=headers, params=params)
    if response.status_code != 200:
        return []

    resultados = response.json().get("results", [])
    return [d for d in resultados if d["properties"].get("id_de_origem")]

def sincronizar_para_origem(deal_tap):
    token = renovar_token_automaticamente()
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    origem_id = deal_tap["properties"].get("id_de_origem")
    if not origem_id:
        return f"❌ Negócio {deal_tap['id']} não tem negócio de origem vinculado."

    propriedades_para_atualizar = {
        campo: deal_tap["properties"].get(campo)
        for campo in CAMPOS_REVERSO
        if deal_tap["properties"].get(campo) is not None
    }

    if not propriedades_para_atualizar:
        return f"⚠️ Negócio {deal_tap['id']} não tem valores a sincronizar."

    url = f"https://api.hubapi.com/crm/v3/objects/deals/{origem_id}"
    body = { "properties": propriedades_para_atualizar }

    response = requests.patch(url, headers=headers, json=body)

    if response.status_code == 200:
        return f"✅ Atualizado: {deal_tap['id']} → {origem_id}"
    else:
        return f"❌ Erro ao atualizar {origem_id}: {response.text}"
