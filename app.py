import streamlit as st
import pandas as pd
import plotly.express as px

# Configuração da Página
st.set_page_config(page_title="Boutique de Perfumes", layout="wide")

# CSS para o estilo Boutique (Rosa e Dourado)
st.markdown("""
    <style>
    .stApp {background-color: #fdf0f5;}
    .produto-card {background: white; padding: 15px; border-radius: 15px; border-left: 5px solid #d4af37; margin-bottom: 15px; box-shadow: 2px 2px 5px rgba(0,0,0,0.1);}
    h1 {color: #b8860b; text-align: center;}
    </style>
""", unsafe_allow_html=True)

# --- CARREGAR DADOS ---
sheet_id = "1-NQNbRKtOeLtw47ThMkobuEwYN8TvFRcvVWgvst_-M0"
url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet=Sheet1"

@st.cache_data(ttl=60)
def carregar_dados():
    df = pd.read_csv(url)
    df.columns = df.columns.str.strip()
    return df

df = carregar_dados()

# --- SIDEBAR (LOGIN) ---
with st.sidebar:
    st.subheader("🔐 Área da Gerente")
    senha = st.text_input("Senha", type="password")

st.title("✨ Boutique de Perfumes")

# --- CATÁLOGO ---
st.markdown("### 🛍️ Escolha seus produtos")
genero = st.selectbox("Filtrar por Categoria:", ["Todos"] + list(df['Categoria'].unique()))

df_f = df if genero == "Todos" else df[df['Categoria'] == genero]

for idx, row in df_f.iterrows():
    st.markdown('<div class="produto-card">', unsafe_allow_html=True)
    
    # Tratamento de erro para o preço
    preco = row['Preco Venda']
    try:
        preco_formatado = f"R$ {float(preco):.2f}"
    except (ValueError, TypeError):
        preco_formatado = "Consultar"

    st.write(f"### {row['Produto']}")
    c1, c2, c3 = st.columns([2, 1, 1])
    c1.write(f"**Preço:** {preco_formatado}")
    
    # Tratamento de erro para o Estoque
    estoque = int(row['Estoque']) if pd.notna(row['Estoque']) else 1
    qtd = c2.number_input("Qtd", 1, estoque, key=f"q{idx}", label_visibility="collapsed")
    
    if c3.button("🛒 Comprar", key=f"btn{idx}"):
        msg = f"Olá, quero {qtd}x {row['Produto']}!"
        st.link_button("Finalizar no Zap", f"https://wa.me/5551993144399?text={msg.replace(' ', '%20')}")
    st.markdown('</div>', unsafe_allow_html=True)

# --- DASHBOARD PROTEGIDO ---
if senha == "1234":
    st.markdown("---")
    st.header("📊 Painel de Controle (Privado)")
    # Cálculo seguro do lucro
    df['Lucro'] = pd.to_numeric(df['Preco Venda'], errors='coerce') - pd.to_numeric(df['Preco Compra'], errors='coerce')
    st.metric("Lucro Total Estimado", f"R$ {df['Lucro'].sum():.2f}")
    st.table(df)
