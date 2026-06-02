import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Boutique Admin", layout="wide")

# CSS para o estilo Boutique
st.markdown("""
    <style>
    .stApp {background-color: #fdf0f5;}
    .produto-card {background: white; padding: 20px; border-radius: 15px; border: 1px solid #d4af37; margin-bottom: 15px;}
    .stButton>button {background-color: #d4af37; color: white;}
    </style>
""", unsafe_allow_html=True)

# CARGA DE DADOS
def load_data(sheet):
    url = f"https://docs.google.com/spreadsheets/d/1-NQNbRKtOeLtw47ThMkobuEwYN8TvFRcvVWgvst_-M0/gviz/tq?tqx=out:csv&sheet={sheet}"
    return pd.read_csv(url)

df_prod = load_data("Produtos")
df_vendas = load_data("Vendas")

# --- ABAS ---
aba1, aba2, aba3 = st.tabs(["🛍️ Catálogo", "👤 Clientes", "🔐 Gestão (Mãe)"])

with aba1:
    # Lógica de Desconto Automático
    df_prod['Preco Final'] = df_prod['Preco Venda'] * (1 - df_prod['Desconto']/100)
    
    filtro = st.selectbox("Categoria:", ["Todos"] + list(df_prod['Categoria'].unique()))
    df_f = df_prod if filtro == "Todos" else df_prod[df_prod['Categoria'] == filtro]
    
    for _, row in df_f.iterrows():
        st.markdown('<div class="produto-card">', unsafe_allow_html=True)
        col1, col2 = st.columns([2,1])
        col1.subheader(row['Produto'])
        if row['Desconto'] > 0:
            col2.write(f"~~R$ {row['Preco Venda']:.2f}~~")
            col2.write(f"### R$ {row['Preco Final']:.2f} (-{row['Desconto']}%)")
        else:
            col2.write(f"### R$ {row['Preco Final']:.2f}")
        st.markdown('</div>', unsafe_allow_html=True)

with aba2:
    st.subheader("Cadastro de Clientes")
    with st.form("c"):
        nome = st.text_input("Nome")
        cpf = st.text_input("CPF")
        tel = st.text_input("Telefone")
        if st.form_submit_button("Cadastrar"):
            st.success(f"Cliente {nome} cadastrado!")

with aba3:
    st.subheader("🔐 Painel de Gestão")
    senha = st.text_input("Senha", type="password")
    if senha == "1234":
        # 1. Ajuste de Descontos
        st.write("### Ajustar Descontos (%)")
        produto_desc = st.selectbox("Produto", df_prod['Produto'])
        novo_desc = st.number_input("Percentual de Desconto", 0, 100)
        if st.button("Aplicar Desconto"):
            st.info(f"Desconto de {novo_desc}% aplicado ao {produto_desc}. (Sincronize com sua Planilha)")
        
        # 2. Dash de Vendas (Funil/Lucro)
        df_vendas['Margem'] = df_vendas['Preco Venda'] - df_vendas['Preco Compra']
        st.subheader("📊 Funil e Margem")
        fig = px.bar(df_vendas, x='Produto', y=['Margem', 'Preco Compra'], title="Margem de Lucro por Produto")
        st.plotly_chart(fig)
        st.table(df_vendas)
