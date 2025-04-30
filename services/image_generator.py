import requests

def gerar_imagem(prompt_visual):
    url = "https://lexica.art/api/v1/search"
    resposta = requests.get(url, params={"q": prompt_visual})
    
    if resposta.status_code == 200:
        dados = resposta.json()
        if dados["images"]:
            return dados["images"][0]["src"]  # pega a primeira imagem da lista
        else:
            return None
    else:
        return None
