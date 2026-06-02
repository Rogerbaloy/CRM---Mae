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
    # A limpeza acontece AQUI dentro, logo após carregar
    df.columns = df.columns.str.strip() 
    return df

# Chama a função
df = carregar_dados()

# 2. Verificação de Segurança (Agora o 'df' já existe!)
colunas_necessarias = ['Produto', 'Preço Venda', 'Preço Pago', 'Categoria', 'Estoque']
for col in colunas_necessarias:
    if col not in df.columns:
        st.error(f"ERRO: A coluna '{col}' não foi encontrada na sua planilha!")
        st.write("Colunas encontradas na planilha:", df.columns.tolist())
        st.stop() # Interrompe a execução para você ler o erro

# 3. Cálculos
df['Lucro'] = df['Preço Venda'] - df['Preço Pago']

# Inicializar carrinho
if 'carrinho' not in st.session_state:
    st.session_state.carrinho = None

# ... (restante do código das abas continua aqui)
