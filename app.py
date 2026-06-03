import streamlit as st
import pandas as pd
def limpar_valor(valor):
    if pd.isna(valor) or valor == '':
        return 0.0
    # Se já for número, retorna ele mesmo
    if isinstance(valor, (int, float)):
        return float(valor)
    # Se for string (ex: "99,99"), troca vírgula por ponto
    valor = str(valor).replace(',', '.')
    try:
        return float(valor)
    except:
        return 0.0
        
# CSS Feminino, Clean e Mobile-Friendly
st.markdown("""
    <style>
    /* Adicione isso dentro do seu bloco <style> */
.block-container {
    padding-top: 1rem !important;
    padding-bottom: 1rem !important;
    padding-left: 1rem !important;
    padding-right: 1rem !important;
}
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700&family=Montserrat:wght@300;400&display=swap');
    
    /* Fundo suave */
    .stApp {background-color: #fdfafb;}
    
    /* Cabeçalho Boutique */
    .header-box {
        text-align: center; 
        padding: 2rem 1rem; 
        background: linear-gradient(135deg, #d4af37 0%, #fce4ec 100%); 
        border-radius: 0 0 30px 30px; 
        margin-bottom: 20px;
        color: #5d4037;
    }
    
    .brand-title {
        font-family: 'Playfair Display', serif; 
        font-size: 2.2em; 
        margin: 0;
    }
    
    .slogan {
        font-family: 'Montserrat', sans-serif;
        font-style: italic;
        font-size: 1em;
        margin-top: 5px;
    }

    /* Cards de produtos minimalistas */
    .produto-card {
        background: white; 
        padding: 15px; 
        border-radius: 20px; 
        border: 1px solid #fce4ec;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05); 
        margin-bottom: 15px;
    }
    </style>
  """, unsafe_allow_html=True)

# Cabeçalho aplicado
st.markdown("""
    <div class="header-box">
        <h1 class="brand-title">Perfumaria & Boutique da Mi</h1>
        <p class="slogan">✨ Elegância em cada detalhe ✨</p>
    </div>
""", unsafe_allow_html=True)

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
            
            # Estoque seguro - Substitua a linha 43 por este bloco:
            estoque_raw = row['Estoque']
            try:
                # Primeiro converte para float (para lidar com 5.0) e depois para int
                estoque_val = int(float(estoque_raw))
            except (ValueError, TypeError):
                # Se for vazio, texto ou qualquer erro, assume 0
                estoque_val = 0
            st.write(f"**Estoque:** {estoque_val}")
            
        with c2:
            # Preço e Desconto seguro
            with c2:
            # Usa a função para limpar Preço e Desconto
             preco_base = limpar_valor(row['Preco Venda'])
             desc = limpar_valor(row['Desconto'])
                
            preco_final = preco_base * (1 - desc/100)
            
            if desc > 0:
                st.write(f"~~R$ {preco_base:.2f}~~")
                st.markdown(f"### <span style='color:red'>R$ {preco_final:.2f}</span>", unsafe_allow_html=True)
            else:
                st.write(f"### R$ {preco_base:.2f}")
                
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
    senha = st.text_input("Senha", type="password", key="senha_admin")
    
    if senha == "1234":
        try:
            # Conexão (Esta parte deve estar correta)
            import gspread
            from oauth2client.service_account import ServiceAccountCredentials
            
            secrets = st.secrets["gcp_service_account"]
            scope = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']
            creds = ServiceAccountCredentials.from_json_keyfile_dict(secrets, scope)
            client = gspread.authorize(creds)
            ws = client.open_by_key("1-NQNbRKtOeLtw47ThMkobuEwYN8TvFRcvVWgvst_-M0").worksheet("Produtos")
            
            # Carregar dados
            dados_produtos = ws.get_all_records()
            df_atualizado = pd.DataFrame(dados_produtos)
            df_atualizado = df_atualizado[df_atualizado['Produto'] != '']
            lista_formatada = [f"Cod {int(row['Codigo'])} - {row['Produto']}" for _, row in df_atualizado.iterrows()]
            
            st.success("Conectado à planilha!")
            
            # Aqui é onde o seu código deve estar para evitar erros de fechamento
            st.write("Sistema pronto para gestão.")

        except Exception as e:
            st.error(f"Erro na conexão: {e}")
