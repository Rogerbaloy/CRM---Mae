import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="CRM Perfumaria", layout="wide")
st.title("✨ CRM de Vendas - Perfumaria")

# 1. Carregar Dados (Planilha)
sheet_id = "1-NQNbRKtOeLtw47ThMkobuEwYN8TvFRcvVWgvst_-M0"
url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet=Sheet1"
df = pd.read_csv(url)

# Cálculos
df['Lucro'] = df['Preço Venda'] - df['Preço Pago']
df['Margem'] = ((df['Lucro'] / df['Preço Venda']) * 100).round(1)

# Abas do Sistema
aba1, aba2, aba3 = st.tabs(["🛍️ Vendas", "📊 Dashboard", "👤 Clientes"])

with aba1: # CATÁLOGO
    st.header("Escolha os produtos")
    genero = st.selectbox("Filtrar Gênero:", ["Todos", "Masculino", "Feminino"])
    df_f = df if genero == "Todos" else df[df['Categoria'] == genero]
    
    for idx, row in df_f.iterrows():
        c1, c2, c3 = st.columns([2, 1, 1])
        c1.write(f"**{row['Produto']}** ({row['Marca']})")
        c2.write(f"R$ {row['Preço Venda']}")
        if c3.button("Comprar", key=f"venda_{idx}"):
            st.session_state.carrinho = row['Produto']
            st.success(f"{row['Produto']} no carrinho!")

with aba2: # DASHBOARD
    st.header("Visão Financeira")
    c1, c2 = st.columns(2)
    c1.metric("Lucro Total Estimado", f"R$ {df['Lucro'].sum():.2f}")
    c2.metric("Produtos em Estoque", df['Estoque'].sum())
    
    fig = px.bar(df, x='Produto', y='Lucro', title="Lucro por Produto")
    st.plotly_chart(fig, use_container_width=True)

with aba3: # CADASTRO
    with st.form("cadastro"):
        nome = st.text_input("Nome do Cliente")
        if st.form_submit_button("Salvar Cliente"):
            st.success(f"Cliente {nome} salvo!")
