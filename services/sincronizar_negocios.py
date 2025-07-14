import requests
from .hubspot_oauth import renovar_token_automaticamente
from .hubspot_pipelines import buscar_id_pipeline_por_nome


STAGE_ID_REQUERIDO = "1105086127"

CAMPOS_REVERSO = [
    "valor_faturado_ano_atual",
    "valor_faturado_proximos_anos"
]

def buscar_negocios_tap():
    token = renovar_token_automaticamente()
    headers = {
        "Authorization": f"Bearer {token}"
    }

    pipeline_id_tap = buscar_id_pipeline_por_nome("TAP & Kickoff")
    if not pipeline_id_tap:
        print("❌ Pipeline 'TAP & Kickoff' não encontrada.")
        return []

    url = "https://api.hubapi.com/crm/v3/objects/deals"
    params = {
        "limit": 100,
        "properties": f"id_de_origem,dealstage,pipeline,{','.join(CAMPOS_REVERSO)}"
    }

    response = requests.get(url, headers=headers, params=params)
    if response.status_code != 200:
        print("❌ Erro ao buscar negócios:", response.text)
        return []

    resultados = response.json().get("results", [])
    filtrados = []

    for d in resultados:
        props = d["properties"]
        if (
            props.get("pipeline") == pipeline_id_tap and
            props.get("dealstage") == STAGE_ID_REQUERIDO and
            props.get("id_de_origem")
        ):
            filtrados.append(d)

    return filtrados

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

    print(f"🔄 Atualizando negócio origem {origem_id} com dados {body}")
    response = requests.patch(url, headers=headers, json=body)

    if response.status_code == 200:
        return f"✅ Atualizado: {deal_tap['id']} → {origem_id}"
    else:
        return f"❌ Erro ao atualizar {origem_id}: {response.status_code} - {response.text}"
