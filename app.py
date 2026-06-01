import streamlit as st
import pandas as pd

st.set_page_config(page_title="CRM Perfumaria", layout="wide")
st.title("✨ CRM de Vendas - Perfumaria")

# URL da sua planilha publicada
sheet_id = "1-NQNbRKtOeLtw47ThMkobuEwYN8TvFRcvVWgvst_-M0"
url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet=Sheet1"

df = pd.read_csv(url)
df.columns = df.columns.str.strip()

st.dataframe(df, use_container_width=True)