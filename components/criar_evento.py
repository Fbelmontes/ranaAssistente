import streamlit as st
from services.hubspot_event_api import criar_evento_marketing
from datetime import datetime

def criar_evento_component():
    st.subheader("📅 Criar Novo Evento de Marketing")
