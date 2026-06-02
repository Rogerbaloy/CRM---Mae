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
# No topo do seu código (na função load_data):
def load_data(sheet):
    try:
        url = f"https://docs.google.com/spreadsheets/d/1-NQNbRKtOeLtw47ThMkobuEwYN8TvFRcvVWgvst_-M0/gviz/tq?tqx=out:csv&sheet={sheet}"
        df = pd.read_csv(url)
        # LIMPEZA: Remove linhas onde o nome do produto ou categoria esteja vazio
        df = df.dropna(subset=['Produto', 'Categoria']) 
        return df
    except: return pd.DataFrame()

df_prod = load_data("Produtos")
df_vendas = load_data("Vendas")

# HEADER CHAMATIVO
st.markdown("""<div class="header-box"><h1 class="brand-title">✨ Perfumaria e Boutique da Mi</h1><p>Elegância em cada gota</p></div>""", unsafe_allow_html=True)

# ABAS
aba1, aba2, aba3 = st.tabs(["🛍️ Catálogo", "👤 Clientes", "🔐 Gestão (Mãe)"])

with c1:
            codigo = int(row['Codigo']) if pd.notna(row['Codigo']) else 0
            st.subheader(f"{row['Marca']} - cod {codigo} {row['Produto']}")
            st.write(f"**Descrição:** {row['Descricao']}")
            
            # --- BLINDAGEM DE ESTOQUE ---
            estoque_raw = row['Estoque']
            estoque_val = int(estoque_raw) if pd.notna(estoque_raw) and str(estoque_raw).replace('.','',1).isdigit() else 0
            st.write(f"**Estoque:** {estoque_val}")
            
with c2:
            # --- BLINDAGEM DE PREÇO ---
            preco_raw = row['Preco Venda']
            preco_base = float(preco_raw) if pd.notna(preco_raw) and str(preco_raw).replace('.','',1).isdigit() else 0.0
            
            # Desconto
            desc_raw = row['Desconto']
            desc = float(desc_raw) if pd.notna(desc_raw) and str(desc_raw).replace('.','',1).isdigit() else 0.0
            
            preco_final = preco_base * (1 - desc/100)
            
            if desc > 0:
                st.write(f"~~R$ {preco_base:.2f}~~")
                st.markdown(f"### <span style='color:red'>R$ {preco_final:.2f}</span>", unsafe_allow_html=True)
            else:
                st.write(f"### R$ {preco_base:.2f}")
                
            # Estoque seguro
            estoque_limite = int(to_float(row['Estoque']))
            qtd = st.number_input("Qtd", 1, max(1, estoque_limite), key=f"q_{idx}")
            
            if st.button("🛒 Adicionar ao Carrinho", key=f"btn_{idx}"):
                item = f"{qtd}x {row['Produto']} (R$ {preco_final:.2f})"
                st.session_state.carrinho.append(item)
                st.success(f"{row['Produto']} adicionado!")
        
            st.markdown('</div>', unsafe_allow_html=True)

    # --- O CARRINHO TAMBÉM DEVE ESTAR RECUADO (DENTRO DA ABA1) ---
    if st.session_state.carrinho:
        st.write("---")
        st.subheader("🛒 Seu Carrinho")
        for item in st.session_state.carrinho:
            st.write(f"- {item}")
        
        msg = "Olá! Gostaria de comprar: " + " | ".join(st.session_state.carrinho)
        st.link_button("Finalizar Pedido via WhatsApp", f"https://wa.me/5551997812374?text={msg}")
        
        if st.button("Limpar Carrinho"):
            st.session_state.carrinho = []
            st.rerun()
with aba2:
    st.subheader("Cadastro de Clientes")
    with st.form("c"):
        nome = st.text_input("Nome"); cpf = st.text_input("CPF"); tel = st.text_input("Telefone")
        if st.form_submit_button("Cadastrar"): st.success("Cliente salvo!")

with aba3:
    st.subheader("🔐 Painel Exclusivo da Mi")
    senha = st.text_input("Senha", type="password", key="senha_admin")
    
    if senha == "1234":
        try:
            import gspread
            from oauth2client.service_account import ServiceAccountCredentials
            
            secrets = st.secrets["gcp_service_account"]
            scope = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']
            creds = ServiceAccountCredentials.from_json_keyfile_dict(secrets, scope)
            client = gspread.authorize(creds)
            ws = client.open_by_key("1-NQNbRKtOeLtw47ThMkobuEwYN8TvFRcvVWgvst_-M0").worksheet("Produtos")
            
            dados_produtos = ws.get_all_records()
            df_atualizado = pd.DataFrame(dados_produtos)
            df_atualizado = df_atualizado[df_atualizado['Produto'] != '']
            
            # CRIAMOS A LISTA FORMATADA: "Cod X - Nome"
            lista_formatada = [f"Cod {int(row['Codigo'])} - {row['Produto']}" for _, row in df_atualizado.iterrows()]
            
            # --- BLOCO 1: APLICAR DESCONTO ---
            with st.expander("🏷️ Aplicar Desconto em Produto"):
                selecionado = st.selectbox("Escolha o produto:", lista_formatada, key="desc_prod")
                cod_extraido = int(selecionado.split(" - ")[0].replace("Cod ", ""))
                desc_sel = st.number_input("Novo Desconto (%)", 0, 100, key="desc_val")
                
                if st.button("Confirmar Desconto"):
                    cell = ws.find(str(cod_extraido), in_column=1) # Busca na coluna 1 (Código)
                    ws.update_cell(cell.row, 7, desc_sel)
                    st.success(f"Desconto aplicado ao produto {selecionado}!")
                    st.rerun()

            # --- BLOCO 2: REGISTRAR VENDA ---
            with st.expander("📉 Registrar Venda (Baixa de Estoque)"):
                prod_venda = st.selectbox("Produto Vendido:", lista_formatada, key="venda_prod")
                cod_venda = int(prod_venda.split(" - ")[0].replace("Cod ", ""))
                qtd_venda = st.number_input("Quantidade Vendida:", 1, 100, key="venda_qtd")
                
                if st.button("Registrar Venda"):
                    cell = ws.find(str(cod_venda), in_column=1)
                    estoque_atual = int(ws.cell(cell.row, 8).value)
                    if estoque_atual >= qtd_venda:
                        ws.update_cell(cell.row, 8, estoque_atual - qtd_venda)
                        st.success("Venda registrada!")
                        st.rerun()
                    else:
                        st.error("Estoque insuficiente!")

            # --- BLOCO 3: REPOSIÇÃO ---
            with st.expander("➕ Repor Estoque"):
                prod_repo = st.selectbox("Escolher perfume:", lista_formatada, key="repo_prod")
                cod_repo = int(prod_repo.split(" - ")[0].replace("Cod ", ""))
                qtd_repo = st.number_input("Quantidade para repor:", 1, 100, key="repo_qtd")
                
                if st.button("Confirmar Reposição"):
                    cell = ws.find(str(cod_repo), in_column=1)
                    estoque_atual = int(ws.cell(cell.row, 8).value)
                    ws.update_cell(cell.row, 8, estoque_atual + qtd_repo)
                    st.success("Reposição feita!")
                    st.rerun()

            # --- BLOCO 4: CADASTRO ---
            with st.expander("➕ Cadastro de Novo Produto"):
                with st.form("form_cadastro"):
                    cat = st.selectbox("Categoria:", ["Masculino", "Feminino", "Infantil", "Outros"])
                    nome_prod = st.text_input("Nome:")
                    marca = st.text_input("Marca:")
                    preco = st.number_input("Preço:", 0.0, 1000.0)
                    estoque_ini = st.number_input("Estoque Inicial:", 0, 999)
                    
                    if st.form_submit_button("Cadastrar Produto"):
                        codigos = [int(x) for x in df_atualizado['Codigo'].tolist() if str(x).isdigit()]
                        novo_codigo = max(codigos) + 1 if codigos else 1
                        ws.append_row([novo_codigo, cat, nome_prod, marca, nome_prod, preco, 0, estoque_ini])
                        st.success("Cadastrado!")
                        st.rerun()
        except Exception as e:
            st.error(f"Erro na gestão: {e}")
