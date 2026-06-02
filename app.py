import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="CRM Boutique", layout="wide")

# --- CARREGAR DADOS ---
# Certifique-se de que sua planilha tenha as abas "Produtos", "Vendas" e "Clientes"
sheet_id = "1-NQNbRKtOeLtw47ThMkobuEwYN8TvFRcvVWgvst_-M0"
def load_data(sheet_name):
    url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}"
    return pd.read_csv(url)

df_prod = load_data("Produtos")
df_vendas = load_data("Vendas")
df_clientes = load_data("Clientes")

# --- INTERFACE ---
aba1, aba2, aba3 = st.tabs(["🛍️ Catálogo", "👤 Clientes", "🔐 Gestão (Mãe)"])

with aba1:
    st.title("🛍️ Catálogo")
    for idx, row in df_prod.iterrows():
        st.markdown(f"**{row['Produto']}** | R$ {row['Preco Venda']}")
        if st.button("Comprar", key=f"c_{idx}"):
            st.link_button("Finalizar no Zap", f"https://wa.me/5551993144399?text=Quero {row['Produto']}")

with aba2:
    st.title("👤 Área do Cliente")
    cpf = st.text_input("Digite seu CPF para ver suas compras:")
    if cpf:
        compras = df_vendas[df_vendas['CPF'] == cpf]
        st.table(compras)
    
    with st.form("cadastro"):
        st.subheader("Novo Cadastro")
        nome = st.text_input("Nome")
        cpf_novo = st.text_input("CPF")
        if st.form_submit_button("Cadastrar"):
            st.success("Cadastro salvo!")

with aba3:
    st.title("🔐 Painel da Gerente")
    senha = st.text_input("Senha", type="password")
    if senha == "1234":
        st.subheader("📊 Dashboard de Vendas")
        st.metric("Lucro Total", f"R$ {(df_vendas['Lucro']).sum():.2f}")
        
        # Gráfico de Margem
        fig = px.bar(df_vendas, x='Produto', y='Lucro', color='Produto', title="Margem por Produto")
        st.plotly_chart(fig)
        
        st.subheader("Registro de Vendas")
        st.table(df_vendas)
