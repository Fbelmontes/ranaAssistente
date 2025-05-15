import requests

def buscar_dados_empresa_linkedin(company_name, access_token):
    """
    Função para buscar dados de uma empresa usando a API do LinkedIn
    """
    url = f"https://api.linkedin.com/v2/organizations?q=vanityName&vanityName={company_name}"
    headers = {
        'Authorization': f'Bearer {access_token}',
        'X-Restli-Protocol-Version': '2.0.0'
    }

    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        empresa_data = response.json()
        dados = {
            "nome": empresa_data.get("localizedName", "Nome não encontrado"),
            "setor": empresa_data.get("industry", "Setor não encontrado"),
            "funcionarios": empresa_data.get("employeeCount", "Número de funcionários não encontrado"),
            "seguidores": empresa_data.get("followersCount", "Seguidores não encontrados"),
            "localizacao": empresa_data.get("locations", "Localização não encontrada")
        }
        return dados
    else:
        return {"erro": f"Erro ao acessar dados da empresa: {response.status_code}"}

def obter_eventos_sales_navigator(access_token, organization_id):
    """
    Requisição para acessar eventos através da API de Sales Navigator.
    """
    url = f"https://api.linkedin.com/v2/organizationEvents?q=organization&organization={organization_id}"
    headers = {
        'Authorization': f'Bearer {access_token}',
        'X-Restli-Protocol-Version': '2.0.0'
    }
    
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        return response.json()  # Retorna os eventos da organização
    else:
        return {"erro": f"Erro ao acessar eventos: {response.status_code}"}

def obter_eventos_linkedin(access_token, organization_id):
    """
    Função para obter eventos de uma organização no LinkedIn com o escopo r_events.
    """
    # URL para obter eventos da organização no LinkedIn (com o escopo r_events)
    url = f"https://api.linkedin.com/v2/events?q=organization&organization={organization_id}"
    
    headers = {
        'Authorization': f'Bearer {access_token}',
        'X-Restli-Protocol-Version': '2.0.0'
    }

    # Fazendo a requisição para acessar os eventos
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        return response.json()  # Retorna os eventos encontrados
    else:
        return {"erro": f"Erro ao acessar eventos: {response.status_code} - {response.text}"}
