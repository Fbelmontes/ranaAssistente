import requests

def obter_eventos_organizacao(access_token, organization_id):
    """
    Função para obter os eventos organizados pela organização no LinkedIn.
    """
    url = f"https://api.linkedin.com/rest/eventsByOrganizer?organizer={organization_id}"
    headers = {
        'Authorization': f'Bearer {access_token}',
        'X-Restli-Protocol-Version': '2.0.0',  # Versão do protocolo
        'LinkedIn-Version': '202301',  # Versão da API no formato correto (YYYYMM)
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return response.json()  # Retorna os eventos da organização
    else:
        return {"erro": f"Erro ao acessar eventos: {response.status_code} - {response.text}"}


def obter_detalhes_evento(access_token, event_id):
    """
    Função para obter detalhes de um evento específico.
    """
    url = f"https://api.linkedin.com/rest/events/{event_id}"
    headers = {
        'Authorization': f'Bearer {access_token}',
        'X-Restli-Protocol-Version': '2.0.0',
        'LinkedIn-Version': '202301',  # Versão da API no formato correto (YYYYMM)
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return response.json()  # Retorna os detalhes do evento
    else:
        return {"erro": f"Erro ao acessar detalhes do evento: {response.status_code} - {response.text}"}
