import streamlit as st
import pandas as pd

# CONFIGURAÇÃO INICIAL DA PÁGINA
st.set_page_config(
    page_title="Dados Eólicos USP",
    page_icon="https://upload.wikimedia.org/wikipedia/commons/thumb/a/ad/Wind-turbine-icon.svg/1200px-Wind-turbine-icon.svg.png",
    layout="wide",
)

PAGES = {
    "Início": [
        st.Page("pages/home.py", title="Início")
    ],
    "Dados": [
        st.Page("pages/data-view.py", title="Sobre os Dados")
    ]
}

pg = st.navigation(PAGES, position="top")
pg.run()


