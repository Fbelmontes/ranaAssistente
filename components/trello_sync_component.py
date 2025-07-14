import streamlit as st
import pandas as pd
import re
from datetime import datetime
from services.trello_api import (
    criar_card,
    atualizar_card,
    buscar_cards_do_board,
    atualizar_descricao_card,
    anexar_texto_na_descricao,  # <-- nova função
    LISTAS_TRELLO
)

from services.google_sheets import conectar_sheets

TRELLO_ABA = "Integração_Trelo"
PLANILHA_BRIEFING_ID = "1R9ob_7olENe70KuM2yjBxTJhVoq0s950HLgmSAQY9OA"
ABA_BRIEFING = "Respostas ao formulário 1"

def trello_sync_component():
    st.subheader("🔄 Integração com Trello")

    # ========== BOTÃO 1: Atualizar o Trello ==========
    if st.button("Atualizar o Trello"):
        st.info("🔍 Lendo tarefas da aba Integração_Trelo...")

        aba = conectar_sheets().worksheet(TRELLO_ABA)
        dados = aba.get_all_records()
        df = pd.DataFrame(dados).fillna('')

        board_id = st.secrets["ID_BOARD_TRELLO"]
        todos_cards = buscar_cards_do_board(board_id)

        cards_atualizados = []
        cards_criados = []
        cards_ignorados = []
        atualizacoes = []  # (linha, ID do Card, status)

        for i, row in df.iterrows():
            titulo = str(row.get("Título da Tarefa", "")).strip()
            descricao = str(row.get("Descrição", "")).strip()
            data_original = str(row.get("Data", "")).strip()
            lista_nome = str(row.get("Lista Trello", "")).strip().upper()
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

            id_lista = LISTAS_TRELLO.get(lista_nome)
            if not id_lista:
                st.error(f"❌ Lista '{lista_nome}' não encontrada.")
                continue

            try:
                card_encontrado = next(
                    (c for c in todos_cards if c["name"].strip().casefold() == titulo.casefold()),
                    None
                )

                if card_encontrado:
                    atualizar_card(
                        card_id=card_encontrado["id"],
                        titulo=titulo,
                        descricao=descricao,
                        data=data_formatada,
                        lista_id=card_encontrado.get("idList", id_lista),
                        cor_hex=cor_hex
                    )
                    atualizacoes.append((i + 2, card_encontrado["id"], "sincronizado"))
                    cards_atualizados.append(titulo)
                else:
                    novo_id = criar_card(
                        titulo=titulo,
                        descricao=descricao,
                        data=data_formatada,
                        lista_id=id_lista,
                        cor_hex=cor_hex
                    )
                    atualizacoes.append((i + 2, novo_id, "sincronizado"))
                    cards_criados.append(titulo)

            except Exception as e:
                st.error(f"Erro com '{titulo}': {e}")
                cards_ignorados.append(titulo)

        # Atualização em lote das colunas E e F
        if atualizacoes:
            range_update = f"E2:F{len(df) + 1}"
            valores = [["", ""] for _ in range(len(df))]
            for linha, id_card, status in atualizacoes:
                idx = linha - 2
                valores[idx] = [id_card, status]
            aba.update(range_update, valores)

        st.markdown("---")
        st.success(f"✅ Atualizados: {len(cards_atualizados)}")
        st.info(f"➕ Criados: {len(cards_criados)}")
        if cards_ignorados:
            st.warning(f"⚠️ Ignorados: {len(cards_ignorados)}")

    # ========== BOTÃO 2: Anexar Briefings ==========  
    if st.button("📎 Anexar Briefing aos Cards"):
        st.info("🔍 Lendo dados da memória da RANA...")

        try:
            aba_cards = conectar_sheets().worksheet(TRELLO_ABA)
            df_cards = pd.DataFrame(aba_cards.get_all_records()).fillna('')

            aba_briefings = conectar_sheets().worksheet("Briefings_RANA")
            df_briefings = pd.DataFrame(aba_briefings.get_all_records()).fillna('')

            cards_anexados = 0

            for i, row in df_cards.iterrows():
                titulo_card = str(row.get("Título da Tarefa", "")).strip()
                card_id = row.get("ID do Card (RANA)", "").strip()

                if not card_id:
                    continue

                dados_briefing = df_briefings[
                    df_briefings["📑 Nome do Projeto/Evento:"].str.strip().str.casefold() == titulo_card.casefold()
                ]

                if not dados_briefing.empty:
                    texto_final = ""
                    for _, linha in dados_briefing.iterrows():
                        for coluna, valor in linha.items():
                            if valor:
                                texto_final += f"- {coluna.strip()}: {str(valor).strip()}\n"

                    anexar_texto_na_descricao(card_id, texto_final)
                    cards_anexados += 1

            st.success(f"📎 Briefings anexados em {cards_anexados} cards.")

        except Exception as e:
            st.error(f"❌ Erro ao anexar briefings: {e}")
