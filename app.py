import streamlit as st
import pandas as pd

# Configuração da Página
st.set_page_config(page_title="CRM da Mãe", layout="wide")

st.title("✨ CRM da Mãe")

# --- PARTE 1: CADASTRO DE CLIENTES ---
st.subheader("Adicionar Novo Cliente")
with st.form("cadastro_cliente"):
    nome = st.text_input("Nome do Cliente")
    tel = st.text_input("Telefone")
    email = st.text_input("E-mail")
    submit = st.form_submit_button("Salvar Cliente")
    
    if submit:
        st.success(f"Cliente {nome} adicionado com sucesso!")

# --- PARTE 2: CATÁLOGO DE PRODUTOS ---
st.markdown("---")
st.header("🛍️ Catálogo de Produtos")

# Link da sua planilha de produtos (certifique-se que ela tenha: Produto, Marca, Categoria, Preço, Estoque)
sheet_id = "1-NQNbRKtOeLtw47ThMkobuEwYN8TvFRcvVWgvst_-M0"
url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet=Sheet1"

# Carregar dados do catálogo
try:
    df_produtos = pd.read_csv(url)
    
    # Filtro de Gênero
    genero = st.selectbox("Filtrar por gênero:", ["Todos", "Masculino", "Feminino"])
    
    if genero != "Todos":
        df_exibicao = df_produtos[df_produtos['Categoria'] == genero]
    else:
        df_exibicao = df_produtos

    # Exibição dos itens
    for index, row in df_exibicao.iterrows():
        col1, col2 = st.columns([3, 1])
        col1.write(f"**{row['Produto']}** | Marca: {row['Marca']} | R$ {row['Preço']:.2f}")
        col1.write(f"Estoque disponível: {row['Estoque']}")
        
        if col2.button("Comprar", key=f"btn_{index}"):
            st.write(f"Você selecionou: {row['Produto']}")

except Exception as e:
    st.error("Erro ao carregar o catálogo. Verifique se a planilha tem as colunas corretas.")
