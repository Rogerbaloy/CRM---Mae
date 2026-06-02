import streamlit as st
import pandas as pd

st.set_page_config(page_title="Boutique CRM", layout="wide")

# --- CARGA E LIMPEZA ---
sheet_id = "1-NQNbRKtOeLtw47ThMkobuEwYN8TvFRcvVWgvst_-M0"
url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet=Sheet1"
df = pd.read_csv(url)
df.columns = df.columns.str.strip()

# --- LÓGICA DE COMPRA ---
if 'historico_vendas' not in st.session_state:
    st.session_state.historico_vendas = []

st.title("✨ Boutique de Perfumes")

aba1, aba2 = st.tabs(["🛍️ Catálogo", "👤 Gestão de Clientes"])

with aba1:
    genero = st.selectbox("Filtrar Categoria:", df['Categoria'].unique())
    df_f = df[df['Categoria'] == genero]
    
    for idx, row in df_f.iterrows():
        with st.container():
            st.markdown(f"### {row['Produto']} - {row['Marca']}")
            st.caption(f"Descrição: {row['Descricao']}")
            
            c1, c2, c3 = st.columns([1, 1, 1])
            preco = float(row['Preco Venda'])
            c1.write(f"**R$ {preco:.2f}**")
            
            qtd = c2.number_input("Qtd", 1, int(row['Estoque']), key=f"qtd_{idx}")
            
            # Selo de Desconto
            if qtd >= 2:
                c3.markdown("### 🏷️ 5% OFF!")
                preco_final = (preco * qtd) * 0.95
            else:
                preco_final = preco * qtd
                
            if c3.button("🛒 Comprar", key=f"btn_{idx}"):
                st.session_state.historico_vendas.append({"Produto": row['Produto'], "Qtd": qtd, "Total": preco_final})
                st.success("Adicionado ao carrinho!")
                st.link_button("Finalizar Pedido no Zap", f"https://wa.me/5551993144399?text=Quero {qtd}x {row['Produto']} por R${preco_final:.2f}")

with aba2:
    st.subheader("Clientes e Vendas")
    nome = st.text_input("Nome do Cliente")
    cpf = st.text_input("CPF")
    if st.button("Salvar Registro de Cliente"):
        st.write(f"Registro: {nome} (CPF: {cpf}) comprou itens.")
    
    st.write("### Histórico de Vendas da Sessão")
    st.table(pd.DataFrame(st.session_state.historico_vendas))
