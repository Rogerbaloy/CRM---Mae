import streamlit as st
import pandas as pd

st.set_page_config(page_title="Perfumaria e Boutique da Mi", layout="wide")

# CSS para o estilo "Perfumaria Boutique"
st.markdown("""
    <style>
    .stApp {background-color: #fff5f7;}
    .header-box {text-align: center; padding: 30px; background: linear-gradient(to right, #d4af37, #fdf0f5, #d4af37); border-radius: 15px; margin-bottom: 30px;}
    .brand-title {font-family: 'Playfair Display', serif; font-size: 3em; color: #5d4037; font-weight: bold;}
    .produto-card {background: white; padding: 25px; border-radius: 20px; border: 1px solid #d4af37; box-shadow: 0 4px 15px rgba(0,0,0,0.1); margin-bottom: 20px;}
    </style>
""", unsafe_allow_html=True)

# CARGA DE DADOS
def load_data(sheet):
    try:
        url = f"https://docs.google.com/spreadsheets/d/1-NQNbRKtOeLtw47ThMkobuEwYN8TvFRcvVWgvst_-M0/gviz/tq?tqx=out:csv&sheet={sheet}"
        return pd.read_csv(url)
    except: return pd.DataFrame()

df_prod = load_data("Produtos")
df_vendas = load_data("Vendas")

# HEADER CHAMATIVO
st.markdown("""<div class="header-box"><h1 class="brand-title">✨ Perfumaria e Boutique da Mi</h1><p>Elegância em cada gota</p></div>""", unsafe_allow_html=True)

# ABAS
aba1, aba2, aba3 = st.tabs(["🛍️ Catálogo", "👤 Clientes", "🔐 Gestão (Mãe)"])

with aba1:
    filtro = st.selectbox("Filtrar por Categoria:", ["Todos"] + list(df_prod['Categoria'].unique()))
    df_f = df_prod if filtro == "Todos" else df_prod[df_prod['Categoria'] == filtro]
    
    for idx, row in df_f.iterrows():
        st.markdown('<div class="produto-card">', unsafe_allow_html=True)
        c1, c2 = st.columns([3, 1])
        with c1:
            st.subheader(f"🌸 {row['Produto']} - {row['Marca']}")
            st.write(f"**Descrição:** {row['Descricao']}")
            st.write(f"**Estoque:** {int(row['Estoque'])}")
        with c2:
            preco_base = float(row['Preco Venda'])
            desc = float(row['Desconto'])
            preco_final = preco_base * (1 - desc/100)
            
            if desc > 0:
                st.write(f"~~R$ {preco_base:.2f}~~")
                st.markdown(f"### <span style='color:red'>R$ {preco_final:.2f}</span>", unsafe_allow_html=True)
                st.caption(f"Oferta: -{int(desc)}%")
            else:
                st.write(f"### R$ {preco_final:.2f}")
                
            qtd = st.number_input("Qtd", 1, int(row['Estoque']), key=f"q_{idx}")
            if st.button("🛒 Comprar via WhatsApp", key=f"btn_{idx}"):
                st.link_button("Finalizar Pedido", f"https://wa.me/5551993144399?text=Olá! Quero {qtd}x {row['Produto']}")
        st.markdown('</div>', unsafe_allow_html=True)

with aba2:
    st.subheader("Cadastro de Clientes")
    with st.form("c"):
        nome = st.text_input("Nome"); cpf = st.text_input("CPF"); tel = st.text_input("Telefone")
        if st.form_submit_button("Cadastrar"): st.success("Cliente salvo!")

with aba3:
    st.subheader("🔐 Painel Exclusivo da Mi")
    senha = st.text_input("Senha", type="password", key="senha_admin")
    
if senha == "1234":
    st.write("---")
                st.subheader("📉 Registrar Venda (Baixa de Estoque)")
                
                # Seleciona o produto e a quantidade vendida
                prod_venda = st.selectbox("Produto Vendido:", lista_produtos, key="venda_prod")
                qtd_venda = st.number_input("Quantidade Vendida:", 1, 100, key="venda_qtd")
                
                if st.button("Registrar Venda"):
                    # Encontra a célula do produto
                    cell = ws.find(prod_venda)
                    
                    # Lê o estoque atual (Coluna H na sua planilha, que é a 8ª coluna)
                    estoque_atual = int(ws.cell(cell.row, 8).value)
                    
                    if estoque_atual >= qtd_venda:
                        # Faz a subtração
                        novo_estoque = estoque_atual - qtd_venda
                        
                        # Atualiza a planilha
                        ws.update_cell(cell.row, 8, novo_estoque)
                        
                        # (Opcional) Poderíamos aqui adicionar uma linha na aba 'Vendas' 
                        # com data, cliente e valor, se você quiser um histórico.
                        
                        st.success(f"Venda registrada! Estoque de {prod_venda} atualizado para {novo_estoque}.")
                        st.rerun()
                    else:
                        st.error("Erro: Estoque insuficiente!")
            try:
                # ... (sua parte de conexão que já está funcionando)
                
                st.write("---")
                st.subheader("🏷️ Aplicar Desconto em Produto")
                
                # Cria o seletor com a lista de produtos que vem da planilha
                lista_produtos = df_prod['Produto'].tolist()
                prod_sel = st.selectbox("Escolha o perfume:", lista_produtos)
                
                # Campo para ela digitar o desconto
                desc_sel = st.number_input("Novo Desconto (%)", 0, 100)
                
                if st.button("Confirmar Desconto"):
                    # Busca a linha do produto selecionado na planilha
                    cell = ws.find(prod_sel)
                    
                    # Atualiza a coluna 7 (Coluna G: Desconto) com o novo valor
                    ws.update_cell(cell.row, 7, desc_sel)
                    
                    st.success(f"Desconto de {desc_sel}% aplicado ao {prod_sel} com sucesso!")
                    
                    # O segredo: isso força o site a recarregar e buscar os novos dados
                    st.rerun() 
                    
            except Exception as e:
                st.error(f"Erro ao aplicar desconto: {e}")
