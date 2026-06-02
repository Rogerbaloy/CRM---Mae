import streamlit as st
import pandas as pd

# Configuração de Layout
st.set_page_config(page_title="Boutique de Perfumes", layout="wide")

# CSS para o estilo "Boutique" (Rosa e Dourado)
st.markdown("""
    <style>
    .stApp {background-color: #fdf0f5;}
    .produto-card {background: white; padding: 20px; border-radius: 20px; border: 2px solid #d4af37; margin-bottom: 20px; box-shadow: 3px 3px 10px rgba(0,0,0,0.1);}
    .stButton>button {background-color: #d4af37; color: white; border-radius: 10px;}
    </style>
""", unsafe_allow_html=True)

# --- CARREGAR DADOS ---
sheet_id = "1-NQNbRKtOeLtw47ThMkobuEwYN8TvFRcvVWgvst_-M0"
url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet=Sheet1"
df = pd.read_csv(url)
df.columns = df.columns.str.strip()

# --- SIDEBAR (LOGIN E CONSULTA) ---
with st.sidebar:
    st.markdown("### 🔐 Área da Gerente")
    senha = st.text_input("Senha Admin", type="password")
    st.markdown("---")
    st.markdown("### 👤 Área da Cliente")
    cpf_consulta = st.text_input("Consulte suas compras por CPF:")
    if cpf_consulta:
        st.info(f"Buscando compras para CPF: {cpf_consulta}...")

st.title("✨ Boutique de Perfumes")

# --- CATÁLOGO ---
st.markdown("### 🛍️ Escolha seus produtos")
genero = st.selectbox("Filtrar por Categoria:", ["Todos"] + list(df['Categoria'].unique()), label_visibility="visible")

# Filtro dos dados
df_f = df if genero == "Todos" else df[df['Categoria'] == genero]

# Adicionamos um pequeno espaço controlado em vez de deixar o Streamlit criar um grande
st.write("")

for idx, row in df_f.iterrows():
    with st.container():
        c1, c2, c3 = st.columns([2, 1, 1])
        c1.markdown(f"### {row['Produto']} - {row['Marca']}")
       # ONDE ESTÁ: 
# c1.write(f"Preço: R$ {float(row['Preco Venda']):.2f}")

# SUBSTITUA POR ISSO:
preco = row['Preco Venda']
if pd.isna(preco) or preco == "":
    preco_formatado = "Consultar"
else:
    preco_formatado = f"R$ {float(preco):.2f}"

c1.write(f"**Preço:** {preco_formatado}")
        
        # Quantidade menor
        qtd = c3.number_input("Qtd", 1, int(row['Estoque']), key=f"q{idx}", label_visibility="collapsed")
        
        if qtd >= 2:
            c3.markdown("##### 🏷️ 5% OFF!")
        
        if c3.button("🛒 Comprar", key=f"btn{idx}"):
            st.link_button("Finalizar no Zap", f"https://wa.me/5551993144399?text=Olá, quero {qtd}x {row['Produto']}!")
        st.markdown('</div>', unsafe_allow_html=True)

# --- DASHBOARD PROTEGIDO ---
if senha == "1234":
    with st.expander("📦 Baixar Estoque Manualmente"):
        produto_baixa = st.selectbox("Selecione o produto para dar baixa:", df['Produto'].tolist())
        qtd_baixa = st.number_input("Quantidade vendida:", 1, 100)
        
        if st.button("Confirmar Venda e Baixar Estoque"):
            # Aqui o sistema deduz a quantidade na memória
            st.write(f"Baixa realizada: {qtd_baixa} unidades de {produto_baixa}.")
            st.warning("Para salvar na planilha, sua mãe deve atualizar o Google Sheets manualmente ou usaremos um script de escrita na próxima etapa.")
