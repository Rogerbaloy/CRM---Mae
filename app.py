import streamlit as st
import pandas as pd

st.set_page_config(page_title="Teste de Funcionamento", layout="wide")

# CARGA DE DADOS
def load_data(sheet):
    try:
        url = f"https://docs.google.com/spreadsheets/d/1-NQNbRKtOeLtw47ThMkobuEwYN8TvFRcvVWgvst_-M0/gviz/tq?tqx=out:csv&sheet={sheet}"
        return pd.read_csv(url)
    except: 
        return pd.DataFrame()

df_prod = load_data("Produtos")

st.title("Teste de Execução")

aba1, aba2 = st.tabs(["🛍️ Catálogo", "👤 Clientes"])

with aba1:
    st.write("Catálogo funcionando")

with aba2:
    st.write("Clientes funcionando")
