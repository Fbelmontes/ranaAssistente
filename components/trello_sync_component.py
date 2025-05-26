import streamlit as st
import pandas as pd
from services.trello_api import criar_card, atualizar_card
from services.google_sheets import conectar_sheets

TRELLO_ABA = "Integração_Trelo"


def trello_sync_component():
    st.subheader("🔄 Integração com Trello")

    if st.button("Atualizar o Trello"):
        st.info("Lendo tarefas da aba Integração_Trelo...")

        aba = conectar_sheets().worksheet(TRELLO_ABA)
        dados = aba.get_all_records()
        df = pd.DataFrame(dados)

        for i, row in df.iterrows():
            titulo = row.get("Título da Tarefa", "").strip()
            descricao = str(row.get("Descrição", "")).strip()
            data = row.get("Data", "").strip()
            lista = row.get("Lista Trello", "").strip().upper()
            card_id = row.get("ID do Card (RANA)", "").strip()
            status = row.get("Status", "").strip().lower()

            try:
                if card_id and status == "sincronizado":
                    atualizar_card(card_id, titulo, descricao, data, lista)
                    st.success(f"✅ Atualizado: {titulo},✅ Card ID:{card_id}")
                else:
                    novo_id = criar_card(titulo, descricao, data, lista)
                    aba.update_cell(i + 2, 5, novo_id)       # Coluna E = ID do Card (RANA)
                    aba.update_cell(i + 2, 6, "sincronizado")  # Coluna F = Status
                    st.success(f"🔃 Criado: {titulo}")

            except Exception as e:
                st.error(f"Erro com '{titulo}': {e}")
