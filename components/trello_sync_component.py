import streamlit as st
import pandas as pd
import re
from datetime import datetime
from services.trello_api import criar_card, atualizar_card, buscar_cards_do_board, LISTAS_TRELLO
from services.google_sheets import conectar_sheets

TRELLO_ABA = "Integração_Trelo"

def trello_sync_component():
    st.subheader("🔄 Integração com Trello")

    aba = conectar_sheets().worksheet(TRELLO_ABA)
    dados = aba.get_all_records()
    df = pd.DataFrame(dados).fillna('')

    # Exibir cards sincronizados e pendentes
    sincronizados = df[df["Status"].str.lower() == "sincronizado"]
    pendentes = df[df["Status"].str.lower() != "sincronizado"]

    st.markdown(f"✅ **Tarefas sincronizadas:** {len(sincronizados)}")
    st.markdown(f"❌ **Tarefas pendentes:** {len(pendentes)}")

    if st.button("Atualizar o Trello"):
        st.info("Lendo tarefas da aba Integração_Trelo...")

        # Busca todos os cards do board para evitar duplicações
        todos_cards_board = buscar_cards_do_board()

        for i, row in df.iterrows():
            titulo = str(row.get("Título da Tarefa", "")).strip()
            descricao = str(row.get("Descrição", "")).strip()
            data_original = str(row.get("Data", "")).strip()
            lista_nome = str(row.get("Lista Trello", "")).strip().upper()
            card_id = str(row.get("ID do Card (RANA)", "")).strip()

            # Valida e formata data
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

            id_lista = LISTAS_TRELLO.get(lista_nome)
            if not id_lista:
                st.error(f"Lista '{lista_nome}' não encontrada no mapeamento.")
                continue

            try:
                # Procura o card no board todo
                card_encontrado = next((c for c in todos_cards_board if c["name"].strip().casefold() == titulo.strip().casefold()), None)

                if card_encontrado:
                    atualizar_card(card_encontrado["id"], titulo, descricao, data_formatada, lista_nome)
                    aba.update_cell(i + 2, 5, card_encontrado["id"])
                    aba.update_cell(i + 2, 6, "sincronizado")
                    st.success(f"✅ Atualizado: {titulo}")
                else:
                    novo_id = criar_card(titulo, descricao, data_formatada, lista_nome)
                    aba.update_cell(i + 2, 5, novo_id)
                    aba.update_cell(i + 2, 6, "sincronizado")
                    st.success(f"🔃 Criado: {titulo}")

            except Exception as e:
                st.error(f"Erro com '{titulo}': {e}")
