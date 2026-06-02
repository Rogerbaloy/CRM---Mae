import streamlit as st
import pandas as pd
import plotly.express as px

# Layout Estilo Perfumaria
st.set_page_config(page_title="Loja de Perfumes", layout="wide")
st.markdown("""
    <style>
    .main {background-color: #fdf6f7;}
    .stButton>button {width: 100%; border-radius: 20px; background-color: #d4af37; color: white;}
    .produto-card {padding: 15px; border-radius: 10px; border: 1px solid #ddd; margin-bottom: 10px; background: white;}
    </style>
""", unsafe_allow_html=True)

st.title("✨ Boutique de Perfumes")

# Carregar Dados
sheet_id = "1-NQNbRKtOeLtw47ThMkobuEwYN8TvFRcvVWgvst_-M0"
url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet=Sheet1"
df = pd.read_csv(url)
df.columns = df.columns.str.strip()

# Abas
aba1, aba2, aba3 = st.tabs(["🛍️ Catálogo", "📊 Financeiro", "👤 Clientes"])

with aba1:
    genero = st.selectbox("Filtrar por:", ["Todos", "Masculino", "Feminino"])
    df_f = df if genero == "Todos" else df[df['Categoria'] == genero]
    
    for idx, row in df_f.iterrows():
        with st.container():
            st.markdown('<div class="produto-card">', unsafe_allow_html=True)
            c1, c2, c3, c4 = st.columns([3, 1, 1, 1])
            c1.write(f"**{row['Produto']}**")
            c2.write(f"R$ {row['Preço Venda']:.2f}")
            qtd = c3.number_input("Qtd", 1, int(row['Estoque']), key=f"qtd_{idx}")
            
            if qtd >= 2:
                preco_final = (row['Preço Venda'] * qtd) * 0.95
                c2.write(f"🏷️ -5%: R$ {preco_final:.2f}")
            
            if c4.button("🛒 Comprar", key=f"btn_{idx}"):
                msg = f"Olá! Quero comprar {qtd}x {row['Produto']}. Obrigado pela compra, volte sempre!"
                st.link_button("Finalizar no Zap", f"https://wa.me/5551993144399?text={msg.replace(' ', '%20')}")
            st.markdown('</div>', unsafe_allow_html=True)

with aba3:
    st.header("Cadastro de Cliente")
    with st.form("cadastro"):
        nome = st.text_input("Nome Completo")
        cpf = st.text_input("CPF")
        cel = st.text_input("Número (WhatsApp)")
        if st.form_submit_button("Cadastrar"):
            st.success(f"Cliente {nome} cadastrado!")
