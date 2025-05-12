import requests

# Função para buscar dados sobre a empresa no LinkedIn
def buscar_dados_empresa_linkedin(company_name, access_token):
    """
    Função para buscar dados detalhados de uma empresa no LinkedIn.
    """
    url = f"https://api.linkedin.com/v2/organizations?q=vanityName&vanityName={company_name}"

    headers = {
        "Authorization": f"Bearer {access_token}",
        "X-Restli-Protocol-Version": "2.0.0"
    }

    try:
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
            return {"erro": "Erro ao acessar dados da empresa."}
    except Exception as e:
        return {"erro": f"Erro na chamada à API: {e}"}
