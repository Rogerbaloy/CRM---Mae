import streamlit as st
import pandas as pd

st.set_page_config(page_title="Teste de Funcionamento", layout="wide")

# CARGA DE DADOS
def load_data(sheet):
    try:
        url = f"https://docs.google.com/spreadsheets/d/1-NQNbRKtOeLtw47ThMkobuEwYN8TvFRcvVWgvst_-M0/gviz/tq?tqx=out:csv&sheet={sheet}"
        return pd.read_csv(url)
    except: 
        return pd.DataFrame()

df_prod = load_data("Produtos")

st.title("Teste de Execução")

# ABAS
aba1, aba2, aba3 = st.tabs(["🛍️ Catálogo", "👤 Clientes", "🔐 Gestão (Mãe)"])

with aba1:
    # 1. Filtro
    filtro = st.selectbox("Filtrar por Categoria:", ["Todos", "Masculino", "Feminino", "Infantil", "Outros"])
    df_f = df_prod if filtro == "Todos" else df_prod[df_prod['Categoria'] == filtro]
    
    # 2. Inicialização do Carrinho
    if 'carrinho' not in st.session_state:
        st.session_state.carrinho = []

    # 3. Exibição dos Produtos
    for idx, row in df_f.iterrows():
        if pd.isna(row['Produto']): continue
        
        st.markdown('<div class="produto-card">', unsafe_allow_html=True)
        c1, c2 = st.columns([3, 1])
        
        with c1:
            codigo = int(row['Codigo']) if pd.notna(row['Codigo']) else 0
            st.subheader(f"{row['Marca']} - cod {codigo} {row['Produto']}")
            st.write(f"**Descrição:** {row['Descricao']}")
            
            # Estoque seguro
            estoque_val = int(row['Estoque']) if pd.notna(row['Estoque']) else 0
            st.write(f"**Estoque:** {estoque_val}")
            
        with c2:
            # Preço e Desconto seguro
            preco_base = float(row['Preco Venda']) if pd.notna(row['Preco Venda']) else 0.0
            desc = float(row['Desconto']) if pd.notna(row['Desconto']) else 0.0
            preco_final = preco_base * (1 - desc/100)
            
            if desc > 0:
                st.write(f"~~R$ {preco_base:.2f}~~")
                st.markdown(f"### <span style='color:red'>R$ {preco_final:.2f}</span>", unsafe_allow_html=True)
            else:
                st.write(f"### R$ {preco_final:.2f}")
                
            qtd = st.number_input("Qtd", 1, 99, key=f"q_{idx}")
            if st.button("🛒 Adicionar", key=f"btn_{idx}"):
                st.session_state.carrinho.append(f"{qtd}x {row['Produto']} (R$ {preco_final:.2f})")
                st.success("Adicionado!")
        
        st.markdown('</div>', unsafe_allow_html=True)

    # 4. Carrinho
    if st.session_state.carrinho:
        st.write("---")
        st.subheader("🛒 Seu Carrinho")
        for item in st.session_state.carrinho:
            st.write(f"- {item}")
        
        msg = "Olá! Gostaria de comprar: " + " | ".join(st.session_state.carrinho)
        st.link_button("Finalizar no WhatsApp", f"https://wa.me/5551997812374?text={msg}")
        
        if st.button("Limpar Carrinho"):
            st.session_state.carrinho = []
            st.rerun()

with aba2:
    st.subheader("👤 Cadastro de Clientes")
    # O "with" abre o formulário
    with st.form("form_cliente"):
        nome = st.text_input("Nome:")
        cpf = st.text_input("CPF:")
        tel = st.text_input("Telefone:")
        
        # O botão TEM que estar alinhado dentro do "with" acima
        submit = st.form_submit_button("Cadastrar Cliente")
        
        # E a ação acontece se o botão for clicado
        if submit:
            st.success(f"Cliente {nome} cadastrado com sucesso!")

        
with aba3:
    st.subheader("🔐 Painel Exclusivo da Mi")
    # A SENHA DEVE ESTAR AQUI DENTRO
    senha = st.text_input("Senha", type="password", key="senha_admin")
    
    if senha == "1234":
        st.write("Acesso liberado! Aqui virão os botões de gestão.")
        with st.expander("🏷️ Aplicar Desconto em Produto"):
                selecionado = st.selectbox("Escolha o produto:", lista_formatada, key="desc_prod")
                cod_extraido = int(selecionado.split(" - ")[0].replace("Cod ", ""))
                desc_sel = st.number_input("Novo Desconto (%)", 0, 100, key="desc_val")
                
                if st.button("Confirmar Desconto"):
                    cell = ws.find(str(cod_extraido), in_column=1)
                    ws.update_cell(cell.row, 7, desc_sel)
                    st.success(f"Desconto aplicado ao produto {selecionado}!")
                    st.rerun()
        try:
            import gspread
            from oauth2client.service_account import ServiceAccountCredentials
            
            # Conexão com Google Sheets
            secrets = st.secrets["gcp_service_account"]
            scope = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']
            creds = ServiceAccountCredentials.from_json_keyfile_dict(secrets, scope)
            client = gspread.authorize(creds)
            ws = client.open_by_key("1-NQNbRKtOeLtw47ThMkobuEwYN8TvFRcvVWgvst_-M0").worksheet("Produtos")
            
            # Carregar dados
            dados_produtos = ws.get_all_records()
            df_atualizado = pd.DataFrame(dados_produtos)
            df_atualizado = df_atualizado[df_atualizado['Produto'] != '']
            
            st.success("Conectado à planilha!")
            
            # Lista para os selects de gestão
            lista_formatada = [f"Cod {int(row['Codigo'])} - {row['Produto']}" for _, row in df_atualizado.iterrows()]
            
            # --- AGORA PODEMOS ADICIONAR OS BLOCOS ABAIXO ---
            st.write("Escolha uma das opções abaixo para gerenciar seu estoque:")
            
        except Exception as e:
            st.error(f"Erro ao conectar: {e}")
