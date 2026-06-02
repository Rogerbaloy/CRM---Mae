import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="CRM Perfumaria", layout="wide")
st.title("✨ CRM de Vendas - Perfumaria")

# 1. Carregar Dados
sheet_id = "1-NQNbRKtOeLtw47ThMkobuEwYN8TvFRcvVWgvst_-M0"
url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet=Sheet1"

@st.cache_data(ttl=60)
def carregar_dados():
    df = pd.read_csv(url)
    df.columns = df.columns.str.strip()
    
    # FORÇAR DADOS A SEREM NÚMEROS (Remove o erro de TypeError)
    for col in ['Preço Venda', 'Preço Pago']:
        if col in df.columns:
            # Remove "R$", espaços, e converte para número
            df[col] = df[col].astype(str).str.replace('R$', '', regex=False).str.replace(',', '.', regex=False)
            df[col] = pd.to_numeric(df[col], errors='coerce')
    
    return df

df = carregar_dados()

# 2. Cálculos (Agora vai funcionar!)
df['Lucro'] = df['Preço Venda'] - df['Preço Pago']

# 3. Inicializar carrinho
if 'carrinho' not in st.session_state:
    st.session_state.carrinho = None

# 4. Abas
aba1, aba2, aba3 = st.tabs(["🛍️ Vendas", "📊 Dashboard", "👤 Clientes"])

with aba1:
    st.header("Escolha os produtos")
    genero = st.selectbox("Filtrar Gênero:", ["Todos", "Masculino", "Feminino"])
    df_f = df if genero == "Todos" else df[df['Categoria'] == genero]
    
    for idx, row in df_f.iterrows():
        c1, c2, c3 = st.columns([3, 1, 1])
        c1.write(f"**{row['Produto']}** | Preço: R$ {row['Preço Venda']}")
        if c3.button("Comprar", key=f"venda_{idx}"):
            st.session_state.carrinho = row['Produto']
            st.rerun()
            
    if st.session_state.carrinho:
        st.success(f"Item no carrinho: {st.session_state.carrinho}")
        msg = f"Olá, quero comprar o perfume {st.session_state.carrinho}"
        st.link_button("Enviar Pedido no Zap", f"https://wa.me/5551993144399?text={msg.replace(' ', '%20')}")

with aba2:
    st.header("Visão Financeira")
    st.metric("Lucro Total", f"R$ {df['Lucro'].sum():.2f}")
    fig = px.bar(df, x='Produto', y='Lucro', title="Lucro por Produto")
    st.plotly_chart(fig)

with aba3:
    with st.form("cadastro"):
        nome = st.text_input("Nome do Cliente")
        if st.form_submit_button("Salvar"):
            st.success(f"Cliente {nome} salvo!")
