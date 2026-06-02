import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Boutique de Perfumes", layout="wide")

st.title("✨ Boutique de Perfumes")

# Carregar Dados
sheet_id = "1-NQNbRKtOeLtw47ThMkobuEwYN8TvFRcvVWgvst_-M0"
url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet=Sheet1"

@st.cache_data(ttl=60)
def carregar_dados():
    df = pd.read_csv(url)
    df.columns = df.columns.str.strip()
    # Limpeza forçada para garantir que preços sejam números
    for col in ['Preço Venda', 'Preço Pago']:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col].astype(str).str.replace('R$', '').str.replace(',', '.'), errors='coerce').fillna(0)
    return df

df = carregar_dados()

# Abas
aba1, aba2, aba3 = st.tabs(["🛍️ Catálogo", "📊 Financeiro", "👤 Clientes"])

with aba1:
    genero = st.selectbox("Filtrar por:", ["Todos", "Masculino", "Feminino"])
    df_f = df if genero == "Todos" else df[df['Categoria'] == genero]
    
    for idx, row in df_f.iterrows():
        # Verificação de segurança para exibição
        preco = row['Preço Venda'] if pd.notnull(row['Preço Venda']) else 0
        
        with st.container():
            c1, c2, c3, c4 = st.columns([3, 1, 1, 1])
            c1.write(f"**{row['Produto']}**")
            c2.write(f"R$ {preco:.2f}")
            qtd = c3.number_input("Qtd", 1, int(row['Estoque']), key=f"qtd_{idx}")
            
            if c4.button("🛒 Comprar", key=f"btn_{idx}"):
                msg = f"Olá! Quero comprar {qtd}x {row['Produto']}. Obrigado pela compra, volte sempre!"
                st.link_button("Finalizar no Zap", f"https://wa.me/5551993144399?text={msg.replace(' ', '%20')}")

with aba2:
    st.header("Visão Financeira")
    df['Lucro'] = df['Preço Venda'] - df['Preço Pago']
    st.metric("Lucro Total", f"R$ {df['Lucro'].sum():.2f}")
    fig = px.bar(df, x='Produto', y='Lucro')
    st.plotly_chart(fig)

with aba3:
    st.header("Cadastro de Cliente")
    with st.form("cadastro"):
        nome = st.text_input("Nome Completo")
        cpf = st.text_input("CPF")
        cel = st.text_input("Número (WhatsApp)")
        if st.form_submit_button("Cadastrar"):
            st.success(f"Cliente {nome} cadastrado!")
