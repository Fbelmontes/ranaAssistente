import requests
from .hubspot_oauth import renovar_token_automaticamente

def buscar_id_pipeline_por_nome(nome_desejado):
    token = renovar_token_automaticamente()
    headers = {
        "Authorization": f"Bearer {token}"
    }

    url = "https://api.hubapi.com/crm/v3/pipelines/deals"
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print("❌ Erro ao buscar pipelines:", response.text)
        return None

    pipelines = response.json().get("results", [])

    for pipeline in pipelines:
        label = pipeline.get("label", "").strip().lower()
        if label == nome_desejado.strip().lower():
            return pipeline.get("id")

    return None
