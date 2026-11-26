# Rode na pasta exemplo/:  streamlit run app.py
import streamlit as st
from rail_nav import Tema, rail_navigation

st.set_page_config(page_title="Exemplo rail_nav", layout="wide")

pagina = rail_navigation(
    inicio=st.Page("Home.py", title="Início", icon=":material/home:", default=True),
    secoes={
        ("Comercial", "groups"): [
            st.Page("pages/vendas.py", title="Vendas", icon=":material/trending_up:"),
            st.Page("pages/clientes.py", title="Clientes", icon=":material/contacts:"),
        ],
        ("Financeiro", "payments"): [
            st.Page("pages/receita.py", title="Receita", icon=":material/calendar_month:"),
        ],
    },
    tema=Tema(fonte="Inter"),  # ex.: Tema(estilo="apple_tv") ou Tema(fonte="Inter", icones_negrito=True)
)
pagina.run()
