import streamlit as st
import pandas as pd

st.set_page_config(page_title="Loja da Mamãe", layout="wide")

# 1. Carregar Dados
sheet_id = "1-NQNbRKtOeLtw47ThMkobuEwYN8TvFRcvVWgvst_-M0"
url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet=Sheet1"
df = pd.read_csv(url)

# Cálculos automáticos
df['Lucro'] = df['Preço Venda'] - df['Preço Pago']
df['% Ganho'] = ((df['Lucro'] / df['Preço Pago']) * 100).round(1)

st.title("🛍️ Catálogo - Boticário, Natura e Avon")

# 2. Filtros e Categorias
genero = st.sidebar.selectbox("Escolha o Grupo:", ["Todos", "Masculino", "Feminino"])
if genero != "Todos":
    df = df[df['Categoria'] == genero] # Certifique-se que sua planilha tenha a coluna 'Categoria'

# 3. Exibição dos Produtos
if 'carrinho' not in st.session_state:
    st.session_state.carrinho = []

for idx, row in df.iterrows():
    col1, col2, col3 = st.columns([3, 1, 1])
    col1.subheader(f"{row['Produto']} ({row['Marca']})")
    col1.write(f"Preço: R$ {row['Preço Venda']} | Lucro: R$ {row['Lucro']} ({row['% Ganho']}%)")
    
    if col2.button(f"Adicionar {row['Produto']}", key=f"btn_{idx}"):
        st.session_state.carrinho.append(row['Produto'])
        st.success("Adicionado!")

# 4. Carrinho e Pedido
st.sidebar.markdown("---")
st.sidebar.subheader("🛒 Seu Carrinho")
st.sidebar.write(st.session_state.carrinho)

if st.session_state.carrinho:
    st.sidebar.subheader("Finalizar Pedido")
    nome = st.sidebar.text_input("Seu Nome:")
    cpf = st.sidebar.text_input("Seu CPF:")
    if st.sidebar.button("Enviar Pedido no WhatsApp"):
        st.sidebar.write(f"Pedido de {nome} (CPF: {cpf}) enviado para a mamãe!")
        # Aqui podemos gerar um link para o WhatsApp automaticamente
