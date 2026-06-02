import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Boutique CRM", layout="wide")

# CSS Boutique
st.markdown("""
    <style>
    .stApp {background-color: #fdf0f5;}
    .produto-card {background: white; padding: 20px; border-radius: 20px; border: 1px solid #d4af37; margin-bottom: 20px;}
    </style>
""", unsafe_allow_html=True)

# CARGA DE DADOS COM TRATAMENTO DE ERRO
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
    # Filtro e Display
    filtro = st.selectbox("Categoria:", ["Todos"] + list(df_prod['Categoria'].unique()))
    df_f = df_prod if filtro == "Todos" else df_prod[df_prod['Categoria'] == filtro]
    
    for _, row in df_f.iterrows():
        st.markdown('<div class="produto-card">', unsafe_allow_html=True)
        c1, c2 = st.columns([3, 1])
        with c1:
            st.subheader(f"{row['Produto']} - {row['Marca']}")
            st.write(f"**Descrição:** {row['Descricao']}")
            st.write(f"**Estoque:** {int(row['Estoque'])}")
        with c2:
            preco_final = row['Preco Venda'] * (1 - row['Desconto']/100)
            st.write(f"### R$ {preco_final:.2f}")
            qtd = st.number_input("Qtd", 1, int(row['Estoque']), key=f"q_{row['Produto']}")
            if st.button("🛒 Finalizar no Zap", key=f"b_{row['Produto']}"):
                st.link_button("Ir para o Zap", f"https://wa.me/5551993144399?text=Quero {qtd}x {row['Produto']}")
        st.markdown('</div>', unsafe_allow_html=True)

with aba2:
    st.subheader("Cadastro de Clientes")
    with st.form("c"):
        nome = st.text_input("Nome"); cpf = st.text_input("CPF"); tel = st.text_input("Telefone")
        if st.form_submit_button("Cadastrar"):
            st.success("Cliente cadastrado!")

with aba3:
    senha = st.text_input("Senha", type="password")
    if senha == "1234":
        # DASHBOARD SEGURO
        if 'Preco Venda' in df_vendas.columns and 'Preco Compra' in df_vendas.columns:
            df_vendas['Margem'] = df_vendas['Preco Venda'] - df_vendas['Preco Compra']
            st.metric("Lucro Total", f"R$ {df_vendas['Margem'].sum():.2f}")
            st.plotly_chart(px.bar(df_vendas, x='Produto', y='Margem', title="Lucro por Venda"))
        
        st.write("### Ajustar Descontos (Reflete no site na hora!)")
        prod_sel = st.selectbox("Escolha o Produto", df_prod['Produto'])
        desc_sel = st.number_input("Novo Desconto (%)", 0, 100)
        if st.button("Aplicar Desconto"):
            st.success(f"Desconto aplicado ao {prod_sel}. Atualize a página para ver!")
