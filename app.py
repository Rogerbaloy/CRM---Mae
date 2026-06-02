import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="CRM Boutique", layout="wide")

# CSS Boutique
st.markdown("""
    <style>
    .stApp {background-color: #fdf0f5;}
    .produto-card {background: white; padding: 20px; border-radius: 20px; border: 1px solid #d4af37; margin-bottom: 20px;}
    </style>
""", unsafe_allow_html=True)

# CARGA DE DADOS
def load_data(sheet):
    try:
        url = f"https://docs.google.com/spreadsheets/d/1-NQNbRKtOeLtw47ThMkobuEwYN8TvFRcvVWgvst_-M0/gviz/tq?tqx=out:csv&sheet={sheet}"
        return pd.read_csv(url)
    except:
        return pd.DataFrame()

df_prod = load_data("Produtos")
df_vendas = load_data("Vendas")

# --- ABAS ---
aba1, aba2, aba3 = st.tabs(["🛍️ Catálogo", "👤 Clientes", "🔐 Gestão (Mãe)"])

with aba1:
    filtro = st.selectbox("Categoria:", ["Todos"] + list(df_prod['Categoria'].unique()))
    df_f = df_prod if filtro == "Todos" else df_prod[df_prod['Categoria'] == filtro]
    
    # Use 'idx' para garantir que cada botão e input tenha uma chave única
    for idx, row in df_f.iterrows():
        st.markdown('<div class="produto-card">', unsafe_allow_html=True)
        c1, c2 = st.columns([3, 1])
        with c1:
            st.subheader(f"{row.get('Produto', '')} - {row.get('Marca', '')}")
            st.write(f"**Descrição:** {row.get('Descricao', '')}")
            st.write(f"**Estoque:** {int(row.get('Estoque', 0))}")
        with c2:
            preco_base = float(row.get('Preco Venda', 0))
            desconto = float(row.get('Desconto', 0))
            preco_final = preco_base * (1 - desconto/100)
            st.write(f"### R$ {preco_final:.2f}")
            
            # CHAVE ÚNICA usando o idx da linha
            qtd = st.number_input("Qtd", 1, int(row.get('Estoque', 1)), key=f"qtd_{idx}")
            if st.button("🛒 Finalizar no Zap", key=f"btn_{idx}"):
                msg = f"Olá! Quero comprar {qtd}x {row.get('Produto', '')}"
                st.link_button("Ir para o Zap", f"https://wa.me/5551993144399?text={msg.replace(' ', '%20')}")
        st.markdown('</div>', unsafe_allow_html=True)

with aba2:
    st.subheader("Cadastro de Clientes")
    with st.form("form_cliente"):
        nome = st.text_input("Nome")
        cpf = st.text_input("CPF")
        tel = st.text_input("Telefone")
        if st.form_submit_button("Cadastrar"):
            st.success(f"Cliente {nome} cadastrado!")

with aba3:
    senha = st.text_input("Senha", type="password")
    if senha == "1234":
        if not df_vendas.empty and 'Preco Venda' in df_vendas.columns:
            st.metric("Lucro Total", f"R$ {(df_vendas['Preco Venda'] - df_vendas['Preco Compra']).sum():.2f}")
            st.plotly_chart(px.bar(df_vendas, x='Produto', y=(df_vendas['Preco Venda'] - df_vendas['Preco Compra'])))
        st.write("### Ajustar Descontos")
        prod_sel = st.selectbox("Produto", df_prod['Produto'])
        desc_sel = st.number_input("Novo Desconto (%)", 0, 100)
        if st.button("Aplicar Desconto"):
            st.info("Desconto aplicado!")
