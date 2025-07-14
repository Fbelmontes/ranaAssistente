
import streamlit as st
import requests
from services.hubspot_oauth import renovar_token_automaticamente

def explorar_negocios_component():
    st.subheader("馃攷 Explorar Pipelines e Neg贸cios")

    token = renovar_token_automaticamente()
    headers = {"Authorization": f"Bearer {token}"}

    # 1. Buscar pipelines
    pipelines_resp = requests.get("https://api.hubapi.com/crm/v3/pipelines/deals", headers=headers)
    pipelines = pipelines_resp.json().get("results", [])

    if not pipelines:
        st.warning("Nenhuma pipeline encontrada.")
        return

    pipeline_opcoes = {p["label"]: p["id"] for p in pipelines}
    pipeline_nome = st.selectbox("Escolha uma pipeline", list(pipeline_opcoes.keys()))
    pipeline_id = pipeline_opcoes[pipeline_nome]

    # 2. Buscar neg贸cios da pipeline
    deals_url = f"https://api.hubapi.com/crm/v3/objects/deals"
    deals_params = {"limit": 100, "properties": "dealname,pipeline", "pipeline": pipeline_id}
    deals_resp = requests.get(deals_url, headers=headers, params=deals_params)
    deals = deals_resp.json().get("results", [])

    if deals:
        opcoes_deals = {d['properties'].get('dealname', f"Sem nome ({d['id']})"): d['id'] for d in deals}
        deal_nome = st.selectbox("Escolha um neg贸cio", list(opcoes_deals.keys()))
        deal_id = opcoes_deals[deal_nome]

        # 3. Buscar propriedades de neg贸cio
        props_resp = requests.get("https://api.hubapi.com/crm/v3/properties/deals", headers=headers)
        propriedades = props_resp.json().get("results", [])
        nomes_props = [p["name"] for p in propriedades]

        # 4. Buscar dados do neg贸cio selecionado
        st.markdown("### 馃搫 Propriedades do neg贸cio")

        deal_resp = requests.get(
            f"https://api.hubapi.com/crm/v3/objects/deals/{deal_id}",
            headers=headers,
            params={"properties": ",".join(nomes_props)}
        )

        if deal_resp.status_code == 200 and "application/json" in deal_resp.headers.get("Content-Type", ""):
            try:
                dados = deal_resp.json().get("properties", {})
                if dados:
                    for k, v in dados.items():
                        st.write(f"🔹 **{k}**: `{v}`")
                else:
                    st.info("Nenhuma variável disponível para este negócio.")
            except Exception as e:
                st.error("Erro ao processar o conteúdo JSON.")
                st.text(deal_resp.text)
        else:
            st.error(f"Erro ao buscar o negócio: {deal_resp.status_code}")
            st.text(deal_resp.text)

    else:
        st.info("Nenhum neg贸cio encontrado nessa pipeline.")
