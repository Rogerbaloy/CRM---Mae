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

with aba1:
    filtro = st.selectbox("Filtrar por Categoria:", ["Todos"] + list(df_prod['Categoria'].unique()))
    df_f = df_prod if filtro == "Todos" else df_prod[df_prod['Categoria'] == filtro]
    
    # Inicializa o carrinho antes do loop
    if 'carrinho' not in st.session_state:
        st.session_state.carrinho = []

    # Substitua seu loop atual por este formato garantido:
for idx, row in df_f.iterrows():
    # Só processa se o produto existir
    if pd.isna(row['Produto']): continue
    
st.markdown('<div class="produto-card">', unsafe_allow_html=True)
    c1, c2 = st.columns([3, 1])
        with c1:
        # Título limpo: Marca - Codigo - Nome
        codigo = int(row['Codigo']) if pd.notna(row['Codigo']) else "0"
        st.subheader(f"{row['Marca']} - cod {codigo} {row['Produto']}")
        st.write(f"**Descrição:** {row['Descricao']}")
        st.write(f"**Estoque:** {int(row['Estoque']) if pd.notna(row['Estoque']) else 0}")
        
        with c2:
            # Pega o valor e limpa se for vazio ou texto estranho
            p_val = row['Preco Venda']
           # Substitua toda essa linha 51 (ou o bloco todo de cálculo do preço) por:
            try:
                p_val = row['Preco Venda']
                preco_base = float(p_val)
            except:
                preco_base = 0.0

            try:
                d_val = row['Desconto']
                desc = float(d_val)
            except:
                desc = 0.0
            
            preco_final = preco_base * (1 - desc/100)
            
            d_val = row['Desconto']
            desc = float(d_val) if pd.notna(d_val) and str(d_val).replace('.','',1).replace(',','').isdigit() else 0.0
            
            preco_final = preco_base * (1 - desc/100)
            
            if desc > 0:
                st.write(f"~~R$ {preco_base:.2f}~~")
                st.markdown(f"### <span style='color:red'>R$ {preco_final:.2f}</span>", unsafe_allow_html=True)
                st.caption(f"Oferta: -{int(desc)}%")
            else:
                st.write(f"### R$ {preco_final:.2f}")
                
            estoque_limite = int(row['Estoque']) if pd.notna(row['Estoque']) and str(row['Estoque']).replace('.','',1).isdigit() else 0
            qtd = st.number_input("Qtd", 1, max(1, estoque_limite), key=f"q_{idx}")
            
            # Botão de Adicionar (dentro do loop)
            if st.button("🛒 Adicionar ao Carrinho", key=f"btn_{idx}"):
                item = f"{qtd}x {row['Produto']} (R$ {preco_final:.2f})"
                st.session_state.carrinho.append(item)
                st.success(f"{row['Produto']} adicionado!")
        st.markdown('</div>', unsafe_allow_html=True)

    # --- DEPOIS QUE O LOOP TERMINAR (Alinhado com o for, fora dele) ---
    if st.session_state.carrinho:
        st.write("---")
        st.subheader("🛒 Seu Carrinho")
        for item in st.session_state.carrinho:
            st.write(f"- {item}")
        
        msg = "Olá! Gostaria de comprar: " + " | ".join(st.session_state.carrinho)
        st.link_button("Finalizar Pedido via WhatsApp", f"https://wa.me/5551993144399?text={msg}")
        
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
            
           # E na sua Aba 3 (Gestão), onde você lê os dados para o cadastro:
           dados_produtos = ws.get_all_records()
           df_atualizado = pd.DataFrame(dados_produtos)
           # Filtra para remover linhas vazias antes de criar a lista de produtos
           df_atualizado = df_atualizado[df_atualizado['Produto'] != '']
           lista_produtos = df_atualizado['Produto'].tolist()
            
            # --- BLOCO 1: APLICAR DESCONTO ---
            with st.expander("🏷️ Aplicar Desconto em Produto"):
                prod_sel = st.selectbox("Escolha o perfume:", lista_produtos, key="desc_prod")
                desc_sel = st.number_input("Novo Desconto (%)", 0, 100, key="desc_val")
                
                if st.button("Confirmar Desconto"):
                    cell = ws.find(prod_sel)
                    ws.update_cell(cell.row, 7, desc_sel)
                    st.success(f"Desconto de {desc_sel}% aplicado ao {prod_sel}!")
                    st.rerun()

            # --- BLOCO 2: REGISTRAR VENDA ---
            with st.expander("📉 Registrar Venda (Baixa de Estoque)"):
                prod_venda = st.selectbox("Produto Vendido:", lista_produtos, key="venda_prod")
                qtd_venda = st.number_input("Quantidade Vendida:", 1, 100, key="venda_qtd")
                
                if st.button("Registrar Venda"):
                    cell = ws.find(prod_venda)
                    estoque_atual = int(ws.cell(cell.row, 8).value)
                    
                    if estoque_atual >= qtd_venda:
                        novo_estoque = estoque_atual - qtd_venda
                        ws.update_cell(cell.row, 8, novo_estoque)
                        st.success(f"Venda registrada! Estoque de {prod_venda} agora é {novo_estoque}.")
                        st.rerun()
                    else:
                        st.error("Erro: Estoque insuficiente!")
                    
            # --- BLOCO 3: REPOSIÇÃO ---
            with st.expander("➕ Repor Estoque"):
                prod_repo = st.selectbox("Escolher perfume:", lista_produtos, key="repo_prod")
                qtd_repo = st.number_input("Quantidade para repor:", 1, 100, key="repo_qtd")
                
                if st.button("Confirmar Reposição"):
                    cell = ws.find(prod_repo)
                    estoque_atual = int(ws.cell(cell.row, 8).value)
                    novo_estoque = estoque_atual + qtd_repo
                    ws.update_cell(cell.row, 8, novo_estoque)
                    st.success(f"Reposição feita! Estoque de {prod_repo} agora é {novo_estoque}.")
                    st.rerun()

          # --- BLOCO 4: CADASTRO ---
            with st.expander("➕ Cadastro de Novo Produto"):
                with st.form("form_cadastro"):
                    cat = st.selectbox("Categoria:", ["Masculino", "Feminino", "Infantil", "Outros"])
                    nome_prod = st.text_input("Nome/Descrição do Produto:")
                    marca = st.text_input("Marca:")
                    preco = st.number_input("Preço de Venda:", 0.0, 1000.0)
                    estoque_ini = st.number_input("Estoque Inicial:", 0, 999)
                    
                    if st.form_submit_button("Cadastrar Produto"):
                        # Verifica se os campos obrigatórios foram preenchidos
                        if nome_prod and marca:
                            codigos = [int(x) for x in df_atualizado['Codigo'].tolist() if str(x).isdigit()]
                            novo_codigo = max(codigos) + 1 if codigos else 1
                            
                            # Prepara a linha
                            nova_linha = [
                                int(novo_codigo), 
                                str(cat), 
                                str(nome_prod), 
                                str(marca), 
                                str(nome_prod), 
                                float(preco), 
                                0.0, 
                                int(estoque_ini)
                            ]
                            
                            # Adiciona apenas UMA vez
                            ws.append_row(nova_linha)
                            
                            st.success(f"Produto {nome_prod} cadastrado com sucesso! (Código: {novo_codigo})")
                            st.rerun()
                        else:
                            st.error("Por favor, preencha o Nome e a Marca!")
            
        except Exception as e:
            st.error(f"Erro na gestão: {e}")
