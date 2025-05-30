import streamlit as st
import pandas as pd
import re
from datetime import datetime
from services.trello_api import criar_card, atualizar_card, buscar_cards_do_board, LISTAS_TRELLO, atualizar_descricao_card
from services.google_sheets import conectar_sheets, conectar_planilha_externa

TRELLO_ABA = "Integração_Trelo"
PLANILHA_BRIEFING_ID = "1R9ob_7olENe70KuM2yjBxTJhVoq0s950HLgmSAQY9OA"
ABA_BRIEFING = "Respostas ao formulário 1"

def trello_sync_component():
    st.subheader("🔁 Integração com Trello")

    col1, col2 = st.columns([1, 1])
    with col1:
        atualizar_trello = st.button("🔄 Atualizar o Trello")
    with col2:
        anexar_briefing = st.button("📎 Anexar Briefing aos Cards")

    if atualizar_trello:
        st.info("🔍 Lendo tarefas da aba Integração_Trelo...")

        aba = conectar_sheets().worksheet(TRELLO_ABA)
        dados = aba.get_all_records()
        df = pd.DataFrame(dados).fillna('')

        board_id = st.secrets["ID_BOARD_TRELLO"]
        todos_cards = buscar_cards_do_board(board_id)

        cards_atualizados = []
        cards_criados = []
        cards_ignorados = []

        for i, row in df.iterrows():
            titulo = str(row.get("Título da Tarefa", "")).strip()
            descricao = str(row.get("Descrição", "")).strip()
            data_original = str(row.get("Data", "")).strip()
            lista_nome_planilha = str(row.get("Lista Trello", "")).strip().upper()
            card_id_planilha = str(row.get("ID do Card (RANA)", "")).strip()
            cor_hex = str(row.get("Cor HEX", "")).strip()

            if re.match(r"^\d{4}-\d{2}-\d{2}$", data_original):
                try:
                    datetime.strptime(data_original, "%Y-%m-%d")
                    data_formatada = f"{data_original}T12:00:00.000Z"
                except ValueError:
                    st.warning(f"⚠️ Data inválida: {data_original} para '{titulo}'")
                    continue
            else:
                st.warning(f"⚠️ Formato de data inválido: '{data_original}' em '{titulo}'")
                continue

            id_lista_planilha = LISTAS_TRELLO.get(lista_nome_planilha)
            if not id_lista_planilha:
                st.error(f"❌ Lista '{lista_nome_planilha}' não encontrada no mapeamento.")
                continue

            try:
                card_encontrado = None
                for c in todos_cards:
                    if c["name"].strip().casefold() == titulo.strip().casefold():
                        card_encontrado = c
                        break

                if card_encontrado:
                    atualizar_card(
                        card_id=card_encontrado["id"],
                        titulo=titulo,
                        descricao=descricao,
                        data=data_formatada,
                        lista_id=card_encontrado.get("idList", id_lista_planilha),
                        cor_hex=cor_hex
                    )
                    aba.update_cell(i + 2, 5, card_encontrado["id"])
                    aba.update_cell(i + 2, 6, "sincronizado")
                    cards_atualizados.append(titulo)
                else:
                    novo_id = criar_card(
                        titulo=titulo,
                        descricao=descricao,
                        data=data_formatada,
                        lista_id=id_lista_planilha,
                        cor_hex=cor_hex
                    )
                    aba.update_cell(i + 2, 5, novo_id)
                    aba.update_cell(i + 2, 6, "sincronizado")
                    cards_criados.append(titulo)

            except Exception as e:
                st.error(f"Erro com '{titulo}': {e}")
                cards_ignorados.append(titulo)

        st.markdown("---")
        st.success(f"✅ Atualizados: {len(cards_atualizados)}")
        st.info(f"➕ Criados: {len(cards_criados)}")
        if cards_ignorados:
            st.warning(f"⚠️ Ignorados: {len(cards_ignorados)}")

    if anexar_briefing:
        st.info("📎 Buscando briefings e adicionando nas descrições dos cards...")

        try:
            aba_cards = conectar_sheets().worksheet(TRELLO_ABA)
            df_cards = pd.DataFrame(aba_cards.get_all_records()).fillna('')
            aba_briefing = conectar_planilha_externa(PLANILHA_BRIEFING_ID).worksheet(ABA_BRIEFING)
            df_briefing = pd.DataFrame(aba_briefing.get_all_records()).fillna('')

            cards_anexados = 0
            for i, row in df_cards.iterrows():
                titulo = str(row.get("Título da Tarefa", "")).strip()
                card_id = row.get("ID do Card (RANA)", "").strip()
                if not card_id:
                    continue

                dados_briefing = df_briefing[df_briefing["📁 Nome do Projeto/Evento:"].str.strip().str.casefold() == titulo.casefold()]

                if not dados_briefing.empty:
                    texto_briefing = "\n\n📁 Briefing Recebido:\n"
                    for _, linha in dados_briefing.iterrows():
                        for coluna, valor in linha.items():
                            if valor:
                                texto_briefing += f"- {coluna.strip()}: {str(valor).strip()}\n"

                    atualizar_descricao_card(card_id, texto_briefing)
                    cards_anexados += 1

            st.success(f"📁 Briefings adicionados em {cards_anexados} cards.")

        except Exception as e:
            st.error(f"Erro ao anexar briefing: {e}")
