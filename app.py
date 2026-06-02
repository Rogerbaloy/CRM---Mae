import streamlit as st
import pandas as pd

st.set_page_config(page_title="Boutique de Perfumes", layout="wide")

# --- ESTILO BOUTIQUE (CSS) ---
st.markdown("""
    <style>
    .stApp {background-color: #fdf0f5;}
    .produto-card {background: #ffffff; padding: 20px; border-radius: 15px; border: 1px solid #d4af37; margin-bottom: 20px; box-shadow: 2px 2px 10px #fce4ec;}
    h1, h2, h3 {color: #a0522d;}
    .stButton>button {background-color: #d4af37; color: white; border-radius: 5px;}
    </style>
""", unsafe_allow_html=True)

# --- CARREGAR DADOS ---
# Certifique-se de que sua planilha tenha as colunas: Produto, Marca, Descricao, Categoria, Preco Venda, Estoque
sheet_id = "1-NQNbRKtOeLtw47ThMkobuEwYN8TvFRcvVWgvst_-M0"
def load_data(sheet_name):
    url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}"
    return pd.read_csv(url)

df_prod = load_data("Produtos")
df_vendas = load_data("Vendas")

# --- SIDEBAR (CPF E GESTÃO) ---
with st.sidebar:
    st.markdown("### 👤 Área da Cliente")
    cpf_consulta = st.text_input("Digite seu CPF:")
    if cpf_consulta and not df_vendas.empty:
        historico = df_vendas[df_vendas['CPF'].astype(str) == cpf_consulta]
        st.dataframe(historico)
    
    st.markdown("---")
    st.markdown("### 🔐 Gestão da Mãe")
    senha = st.text_input("Senha Admin", type="password")

# --- CATÁLOGO ---
st.title("✨ Boutique de Perfumes")

# Filtro por Categoria
categorias = ["Todos"] + list(df_prod['Categoria'].unique())
filtro = st.selectbox("Filtrar por Categoria:", categorias)
df_f = df_prod if filtro == "Todos" else df_prod[df_prod['Categoria'] == filtro]

for idx, row in df_f.iterrows():
    st.markdown('<div class="produto-card">', unsafe_allow_html=True)
    c1, c2 = st.columns([3, 1])
    
    with c1:
        st.subheader(f"{row['Produto']} - {row['Marca']}")
        st.write(f"**Descrição:** {row['Descricao']}")
        st.write(f"**Estoque:** {int(row['Estoque'])} unidades")
        
    with c2:
        st.write(f"### R$ {float(row['Preco Venda']):.2f}")
        if st.button("🛒 Comprar", key=f"btn_{idx}"):
            msg = f"Olá! Quero comprar o perfume {row['Produto']}"
            st.link_button("Finalizar no Zap", f"https://wa.me/5551993144399?text={msg.replace(' ', '%20')}")
    
    st.markdown('</div>', unsafe_allow_html=True)

# --- DASHBOARD (PROTEGIDO) ---
if senha == "1234":
    st.markdown("---")
    st.header("📊 Painel de Vendas")
    st.table(df_vendas)
