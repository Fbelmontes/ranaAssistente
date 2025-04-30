from duckduckgo_search import DDGS

def buscar_web(termo, max_resultados=5):
    resultados = []
    with DDGS() as ddgs:
        for r in ddgs.text(termo, max_results=max_resultados):
            resultados.append({
                "title": r.get("title", ""),
                "href": r.get("href", ""),
                "body": r.get("body", "")
            })
    return resultados
