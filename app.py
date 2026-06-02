import streamlit as st
import pandas as pd
import plotly.express as px

# Configuração da Página
st.set_page_config(page_title="Boutique de Perfumes", layout="centered")

# Estilo Visual (CSS)
st.markdown("""
    <style>
    /* Fundo Rosa Suave */
    .stApp {background-color: #fdf0f5;}
    /* Cards Elegantes */
    .produto-card {background: white; padding: 20px; border-radius: 15px; border-left: 5px solid #d4af37; margin-bottom: 15px; box-shadow: 2px 2px 5px rgba(0,0,0,0.1);}
    /* Títulos */
    h1 {color: #b8860b; text-align: center;}
    </style>
""", unsafe_allow_html=True)

# Carregar Dados
sheet_id = "1-NQNbRKtOeLtw47ThMkobuEwYN8TvFRcvVWgvst_-M0"
url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet=Sheet1"

@st.cache_data(ttl=60)
def carregar():
    df = pd.read_csv(url)
    df.columns = df.columns.str.strip()
    # Limpeza rigorosa para evitar erros de exibição
    cols_preco = ['Preço Venda', 'Preço Pago']
    for col in cols_preco:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col].replace(r'[R$\s]', '', regex=True).replace(',', '.', regex=True), errors='coerce').fillna(0)
    return df

df = carregar()

# Área da Gerente no Sidebar com fundo especial
with st.sidebar:
    st.markdown("""<div style="background-image: url('https://img.freepik.com/fotos-gratis/fundo-texturizado-rosa-claro_53876-90518.jpg'); padding: 20px; border-radius: 10px; color: white;">
    <h3>🔐 Área da Gerente</h3></div>""", unsafe_allow_html=True)
    senha = st.text_input("Senha", type="password")

st.title("✨ Boutique de Perfumes")

# Catálogo
aba1, aba2 = st.tabs(["🛍️ Catálogo", "👤 Cadastro"])

with aba1:
    genero = st.selectbox("Filtrar por gênero:", ["Todos", "Masculino", "Feminino"])
    df_f = df if genero == "Todos" else df[df['Categoria'] == genero]
    
    for idx, row in df_f.iterrows():
        st.markdown(f'<div class="produto-card">', unsafe_allow_html=True)
        st.write(f"### {row['Produto']}")
        c1, c2 = st.columns(2)
        c1.write(f"**Preço:** R$ {float(row['Preço Venda']):.2f}")
        qtd = c2.number_input("Qtd", 1, int(row.get('Estoque', 1)), key=f"q{idx}")
        
        if st.button("🛒 Comprar agora", key=f"btn{idx}"):
            msg = f"Olá! Quero comprar {qtd}x {row['Produto']}."
            st.link_button("Finalizar no WhatsApp", f"https://wa.me/5551993144399?text={msg.replace(' ', '%20')}")
        st.markdown('</div>', unsafe_allow_html=True)

# Dashboard Protegido
if senha == "1234":
    with st.expander("📊 Painel Financeiro"):
        st.metric("Lucro Total", f"R$ {(df['Preço Venda'] - df['Preço Pago']).sum():.2f}")
        st.plotly_chart(px.bar(df, x='Produto', y=df['Preço Venda'] - df['Preço Pago']))

with aba2:
    with st.form("c"):
        st.text_input("Nome"); st.text_input("CPF"); st.form_submit_button("Enviar")
