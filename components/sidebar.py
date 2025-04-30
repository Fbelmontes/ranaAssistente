import streamlit as st

def criar_sidebar():
    st.sidebar.markdown(
        """
        <div style='text-align: center;'>
            <img src='https://media.tenor.com/xUo0zFgMugUAAAAi/robot.gif' width='100'/>
            <h3 style='margin-top: 10px;'>RANA v5</h3>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.sidebar.markdown("### Menu")
    return st.sidebar.radio(
        "",
        ["📚 Aprender sobre um site", "🤖 Fazer uma pergunta", "🎤 Observar Reunião", "🎨 Alternar tema","DENER"],
        index=0
    )
