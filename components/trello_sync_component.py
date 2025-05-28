import streamlit as st
import pandas as pd
import re
from datetime import datetime
from services.trello_api import criar_card, atualizar_card, buscar_cards_do_board, LISTAS_TRELLO
from services.google_sheets import conectar_sheets

TRELLO_ABA = "Integração_Trelo"

def trello_sync_component():
    st.subheader("🔄 Integração com Trello")

    if st.button("Atualizar o Trello"):
        st.info("Lendo tarefas da aba Integração_Trelo...")

        aba = conectar_sheets().worksheet(TRELLO_ABA)
        dados = aba.get_all_records()
        df = pd.DataFrame(dados).fillna('')

        board_id = st.secrets["ID_BOARD_TRELLO"]
        todos_cards = buscar_cards_do_board(board_id)

        cards_sincronizados = []
        cards_para_sincronizar = []

        for i, row in df.iterrows():
            titulo = str(row.get("Título da Tarefa", "")).strip()
            descricao = str(row.get("Descrição", "")).strip()
            data_original = str(row.get("Data", "")).strip()
            lista_nome_planilha = str(row.get("Lista Trello", "")).strip().upper()
            card_id_planilha = str(row.get("ID do Card (RANA)", "")).strip()
            status = str(row.get("Status", "")).strip().lower()

            # Validar e formatar data
            data_formatada = None
            if re.match(r"^\d{4}-\d{2}-\d{2}$", data_original):
                try:
                    datetime.strptime(data_original, "%Y-%m-%d")
                    data_formatada = f"{data_original}T12:00:00.000Z"
                except ValueError:
                    st.warning(f"⚠️ Data inválida (não existe): {data_original} para '{titulo}'")
                    continue
            else:
                st.warning(f"⚠️ Formato de data inválido: '{data_original}' em '{titulo}'")
                continue

            id_lista_planilha = LISTAS_TRELLO.get(lista_nome_planilha)
            if not id_lista_planilha:
                st.error(f"Lista '{lista_nome_planilha}' não encontrada no mapeamento.")
                continue

            # Procurar o card no Trello por nome (independente da lista)
            card_encontrado = None
            for c in todos_cards:
                if c["name"].strip().casefold() == titulo.strip().casefold():
                    card_encontrado = c
                    break

            try:
                if card_encontrado:
                    # Atualiza na lista onde o card está atualmente
                    id_lista_atual = card_encontrado.get("idList", id_lista_planilha)
                    atualizar_card(card_encontrado["id"], titulo, descricao, data_formatada, id_lista_atual)
                    aba.update_cell(i + 2, 5, card_encontrado["id"])
                    aba.update_cell(i + 2, 6, "sincronizado")
                    cards_sincronizados.append(titulo)
                    st.success(f"✅ Atualizado: {titulo}")
                else:
                    novo_id = criar_card(titulo, descricao, data_formatada, id_lista_planilha)
                    aba.update_cell(i + 2, 5, novo_id)
                    aba.update_cell(i + 2, 6, "sincronizado")
                    cards_para_sincronizar.append(titulo)
                    st.success(f"🔃 Criado: {titulo}")

            except Exception as e:
                st.error(f"Erro com '{titulo}': {e}")

        st.markdown("---")
        st.write(f"✅ **Cards atualizados:** {len(cards_sincronizados)}")
        st.write(f"➕ **Cards criados:** {len(cards_para_sincronizar)}")
