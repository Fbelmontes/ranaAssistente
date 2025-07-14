
import streamlit as st
import requests
from services.hubspot_oauth import renovar_token_automaticamente

def painel_dinamico_negocios_component():
    st.subheader("🛠️ Painel de Negócios e Variáveis Editáveis")

    token = renovar_token_automaticamente()
    headers = {"Authorization": f"Bearer {token}"}

    # 1. Buscar pipelines
    pipelines_resp = requests.get("https://api.hubapi.com/crm/v3/pipelines/deals", headers=headers)
    pipelines = pipelines_resp.json().get("results", [])

    if not pipelines:
        st.warning("Nenhuma pipeline encontrada.")
        return

    pipeline_opcoes = {p["label"]: p["id"] for p in pipelines}
    pipeline_nome = st.selectbox("📦 Escolha uma pipeline", list(pipeline_opcoes.keys()))
    pipeline_id = pipeline_opcoes[pipeline_nome]

    # 2. Buscar negócios da pipeline
    deals_url = f"https://api.hubapi.com/crm/v3/objects/deals"
    deals_params = {
        "limit": 50,
        "properties": "dealname,pipeline,dealstage",
        "pipeline": pipeline_id
    }
    deals_resp = requests.get(deals_url, headers=headers, params=deals_params)
    deals = deals_resp.json().get("results", [])

    if not deals:
        st.info("Nenhum negócio encontrado nessa pipeline.")
        return

    opcoes_deals = {d["properties"].get("dealname", f"Sem nome ({d['id']})"): d["id"] for d in deals}
    deal_nome = st.selectbox("📋 Escolha um negócio", list(opcoes_deals.keys()))
    deal_id = opcoes_deals[deal_nome]

    # 3. Buscar propriedades disponíveis
    props_resp = requests.get("https://api.hubapi.com/crm/v3/properties/deals", headers=headers)
    propriedades = props_resp.json().get("results", [])
    nomes_props = [p["name"] for p in propriedades]

    # 4. Buscar dados do negócio selecionado
    deal_resp = requests.get(
        f"https://api.hubapi.com/crm/v3/objects/deals/{deal_id}",
        headers=headers,
        params={"properties": ",".join(nomes_props)}
    )

    st.markdown("### ✏️ Variáveis do negócio (editáveis)")

    if deal_resp.status_code == 200 and "application/json" in deal_resp.headers.get("Content-Type", ""):
        try:
            dados = deal_resp.json().get("properties", {})
            campos_editados = {}
            for prop in nomes_props:
                valor_atual = dados.get(prop, "")
                novo_valor = st.text_input(f"{prop}", valor_atual)
                if novo_valor != valor_atual:
                    campos_editados[prop] = novo_valor

            if campos_editados and st.button("💾 Atualizar negócio"):
                patch_url = f"https://api.hubapi.com/crm/v3/objects/deals/{deal_id}"
                patch_body = {"properties": campos_editados}
                patch_resp = requests.patch(patch_url, headers=headers, json=patch_body)

                if patch_resp.status_code == 200:
                    st.success("Negócio atualizado com sucesso! ✅")
                else:
                    st.error("Erro ao atualizar o negócio.")
                    st.text(patch_resp.text)

        except Exception:
            st.error("Erro ao processar o JSON do negócio.")
            st.text(deal_resp.text)
    else:
        st.error(f"Erro ao buscar dados do negócio. Código: {deal_resp.status_code}")
        st.text(deal_resp.text)
