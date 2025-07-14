
import requests
from .hubspot_oauth import renovar_token_automaticamente

CAMPOS_SINCRONIZADOS = [
    "data_entrega",
    "valor_faturado",
    "responsavel_tecnico"
]

def buscar_negocios_clonados():
    token = renovar_token_automaticamente()
    headers = {
        "Authorization": f"Bearer {token}"
    }

    url = "https://api.hubapi.com/crm/v3/objects/deals"
    params = {
        "limit": 100,
        "properties": f"deal_id_origem,{','.join(CAMPOS_SINCRONIZADOS)}"
    }

    response = requests.get(url, headers=headers, params=params)
    if response.status_code != 200:
        return []

    resultados = response.json().get("results", [])
    return [d for d in resultados if d["properties"].get("deal_id_origem")]

def sincronizar_negocio(deal_clonado):
    token = renovar_token_automaticamente()
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    origem_id = deal_clonado["properties"].get("deal_id_origem")
    if not origem_id:
        return f"Negócio {deal_clonado['id']} não possui origem."

    propriedades_para_atualizar = {
        campo: deal_clonado["properties"].get(campo)
        for campo in CAMPOS_SINCRONIZADOS
        if deal_clonado["properties"].get(campo) is not None
    }

    if not propriedades_para_atualizar:
        return f"Negócio {deal_clonado['id']} não possui campos para atualizar."

    url = f"https://api.hubapi.com/crm/v3/objects/deals/{origem_id}"
    body = {"properties": propriedades_para_atualizar}

    response = requests.patch(url, headers=headers, json=body)

    if response.status_code == 200:
        return f"✅ Atualizado: {deal_clonado['id']} → {origem_id}"
    else:
        return f"❌ Erro ao atualizar {origem_id}: {response.text}"
