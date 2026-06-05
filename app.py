import streamlit as st
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime

# --- CONEXÃO GLOBAL (FORA DE QUALQUER IF OU ABA) ---
secrets = st.secrets["gcp_service_account"]
scope = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_dict(secrets, scope)
client = gspread.authorize(creds) # Agora o 'client' vive aqui e qualquer aba pode usar!

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

st.title(" ")

# ABAS
aba1, aba2, aba3, aba4 = st.tabs(["🛍️ Catálogo", "👤 Clientes", "🔐 Gestão", "📊 Relatórios"])

with tab1:
    st.subheader("🛍️ Nosso Catálogo")
    
    # Busca os produtos da planilha (deve estar conectado globalmente como 'ws' ou 'ws_prod')
    # Certifique-se de que o 'df_prod' está carregado
    
    # Criamos 3 colunas para os produtos ficarem lado a lado
    cols = st.columns(3)
    
    # Iteramos sobre os produtos (exemplo de lógica)
    for i, row in df_prod.iterrows():
        # Usamos o resto da divisão por 3 para alternar as colunas
        col = cols[i % 3]
        
        with col:
            # Container do produto (o "Card")
            with st.container(border=True):
                st.markdown(f"**{row['Produto']}**")
                st.write(f"Marca: {row['Marca']}")
                st.write(f"R$ {float(row['Preco']):,.2f}")
                
                # Se tiver estoque, mostra status
                if int(row['Estoque']) > 0:
                    st.success("Disponível")
                else:
                    st.error("Esgotado")
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
    st.subheader("🔍 Consulte suas Compras")
    cpf_busca = st.text_input("Digite seu CPF (apenas números):")
    
    if cpf_busca:
        try:
            ws_vendas = client.open_by_key("1-NQNbRKtOeLtw47ThMkobuEwYN8TvFRcvVWgvst_-M0").worksheet("Vendas")
            
            # get_all_values() traz uma matriz pura, sem o Pandas tentar adivinhar nada
            todos_os_dados = ws_vendas.get_all_values()
            
            # O cabeçalho é a primeira linha
            cabecalho = todos_os_dados[0]
            # Os dados são o restante
            registros = todos_os_dados[1:]
            
            # Criamos o DataFrame manualmente para ter controle total
            df = pd.DataFrame(registros, columns=cabecalho)
            
            # Limpeza do CPF (Remove espaços, traços e converte para string)
            df['CPF'] = df['CPF'].astype(str).str.strip()
            cpf_limpo = str(cpf_busca).strip()
            
            # Filtra
            resultado = df[df['CPF'] == cpf_limpo]
            
            if not resultado.empty:
                st.success(f"Encontramos {len(resultado)} compra(s)!")
                # Exibimos apenas as colunas que interessam
                st.table(resultado[['Data', 'Produto', 'Preco total']])
            else:
                st.warning("Nenhuma compra encontrada para este CPF.")
                # Debug visual para você ver o que ele leu
                st.write("CPFs lidos na planilha:", df['CPF'].unique())
                
        except Exception as e:
            st.error(f"Erro ao buscar: {e}")         

        
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

            with st.expander("🏷️ Aplicar Desconto em Produto"):
                selecionado = st.selectbox("Escolha o produto:", lista_formatada, key="desc_prod")
                # Extrai o código corretamente
                cod_extraido = int(selecionado.split(" - ")[0].replace("Cod ", ""))
                desc_sel = st.number_input("Novo Desconto (%)", 0, 100, key="desc_val")
                
                if st.button("Confirmar Desconto"):
                    # Busca a linha do produto pelo código na Coluna 1
                    cell = ws.find(str(cod_extraido), in_column=1)
                    
                    # Atualiza a Coluna 8 (Desconto)
                    ws.update_cell(cell.row, 8, desc_sel)
                    
                    st.success(f"Desconto de {desc_sel}% aplicado ao {selecionado}!")
                    # O st.rerun() é fundamental aqui para atualizar o catálogo na hora
                    st.rerun()

            # --- BLOCO: CADASTRO DE NOVO PRODUTO ---
            with st.expander("➕ Cadastro de Novo Produto"):
                with st.form("form_cadastro_novo"):
                    cat = st.selectbox("Categoria:", ["Masculino", "Feminino", "Infantil", "Outros"])
                    nome_prod = st.text_input("Nome/Descrição do Produto:")
                    marca = st.text_input("Marca:")
                    preco = st.number_input("Preço de Venda:", 0.0, 1000.0)
                    estoque_ini = st.number_input("Estoque Inicial:", 0, 999)
                    
                    submit_novo = st.form_submit_button("Cadastrar Produto")
                    
                    if submit_novo:
                        if not nome_prod or not marca:
                            st.error("Por favor, preencha o Nome e a Marca!")
                        else:
                            try:
                                # Define um novo código baseando-se no maior código existente
                                codigos = [int(row['Codigo']) for row in dados_produtos if str(row['Codigo']).isdigit()]
                                novo_codigo = max(codigos) + 1 if codigos else 1
                                
                                # Prepara a linha (ajuste a ordem conforme suas colunas: Cod, Prod, Marca, Desc, Cat, PrecoV, PrecoC, Desc, Estoque)
                                nova_linha = [novo_codigo, nome_prod, marca, nome_prod, cat, preco, 0.0, 0.0, estoque_ini]
                                
                                ws.append_row(nova_linha)
                                st.success(f"Produto {nome_prod} cadastrado com sucesso!")
                                st.rerun()
                            except Exception as e:
                                st.error(f"Erro ao salvar novo produto: {e}")

            # --- BLOCO: REPOR ESTOQUE ---
            with st.expander("➕ Repor Estoque"):
                prod_repo = st.selectbox("Escolher perfume:", lista_formatada, key="repo_prod")
                cod_repo = int(prod_repo.split(" - ")[0].replace("Cod ", ""))
                qtd_repo = st.number_input("Quantidade para repor:", 1, 100, key="repo_qtd")
                
                if st.button("Confirmar Reposição"):
                    try:
                        # Busca o produto na Coluna 1
                        cell = ws.find(str(cod_repo), in_column=1)
                        # Lê o estoque atual na Coluna 9
                        estoque_atual = int(ws.cell(cell.row, 9).value)
                        
                        # Atualiza a Coluna 9 somando a quantidade
                        ws.update_cell(cell.row, 9, estoque_atual + qtd_repo)
                        
                        st.success(f"Reposição feita! Novo estoque: {estoque_atual + qtd_repo}")
                        st.rerun()
                    except Exception as e:
                        st.error(f"Erro na reposição: {e}")
            
            # --- BLOCO: REGISTRAR VENDA (BAIXA DE ESTOQUE) ---
            with st.expander("📉 Registrar Venda (Baixa de Estoque)"):
                # --- NOVO: Seleção de cliente para o histórico ---
                # (Assumindo que você tenha uma lista de clientes ou um input simples)
                nome_cliente = st.text_input("Nome do Cliente (opcional):", "Avulso")

            # --- ADICIONE O INPUT DO CPF AQUI
                cpf_cliente = st.text_input("CPF do Cliente (para consulta no portal):")
                
                prod_venda = st.selectbox("Produto Vendido:", lista_formatada, key="venda_prod")
                cod_venda = int(prod_venda.split(" - ")[0].replace("Cod ", ""))
                qtd_venda = st.number_input("Quantidade Vendida:", 1, 100, key="venda_qtd")
                
                if st.button("Confirmar Venda"):
                    try:
                        # 1. Conectar na aba Produtos e Vendas
                        ws_prod = client.open_by_key("1-NQNbRKtOeLtw47ThMkobuEwYN8TvFRcvVWgvst_-M0").worksheet("Produtos")
                        ws_vendas = client.open_by_key("1-NQNbRKtOeLtw47ThMkobuEwYN8TvFRcvVWgvst_-M0").worksheet("Vendas")
                        
                        # 2. Buscar dados do produto
                        cell = ws_prod.find(str(cod_venda), in_column=1)
                        estoque_atual = int(ws_prod.cell(cell.row, 9).value)
                        preco_venda = float(ws_prod.cell(cell.row, 6).value) 
                        
                        # 3. Cálculo do valor (Calculado AQUI para garantir que existe)
                        valor_total = preco_venda * qtd_venda
                        
                        if estoque_atual >= qtd_venda:
                            # Atualiza estoque
                            ws_prod.update_cell(cell.row, 9, estoque_atual - qtd_venda)
                            
                            # 4. Registrar na aba Vendas
                            from datetime import datetime
                            
                            # A lista abaixo deve bater com as colunas da planilha (A até F)
                            ws_vendas.append_row([
                                str(datetime.now().strftime("%d/%m/%Y %H:%M")), 
                                nome_cliente, 
                                prod_venda, 
                                qtd_venda, 
                                valor_total, 
                                cpf_cliente
                            ])
                            
                            st.success(f"Venda registrada! Valor: R$ {valor_total:.2f}")
                            st.rerun()
                        else:
                            st.error("Estoque insuficiente!")
                    except Exception as e:
                        st.error(f"Erro ao registrar: {e}")
                                    
        except Exception as e:
            st.error(f"Erro na conexão: {e}")

with aba4:
     st.subheader("📈 Dashboard de Vendas e Lucro")
     if st.button("Atualizar Relatório"):
                try:
                    ws_vendas = client.open_by_key("1-NQNbRKtOeLtw47ThMkobuEwYN8TvFRcvVWgvst_-M0").worksheet("Vendas")
                    ws_prod = client.open_by_key("1-NQNbRKtOeLtw47ThMkobuEwYN8TvFRcvVWgvst_-M0").worksheet("Produtos")
                    
                    df_vendas = pd.DataFrame(ws_vendas.get_all_records())
                    df_prod = pd.DataFrame(ws_prod.get_all_records())
                    
                    if not df_vendas.empty:
                        df_vendas['Preco total'] = pd.to_numeric(df_vendas['Preco total'])
                        df_vendas['Quantidade'] = pd.to_numeric(df_vendas['Quantidade'])
                        
                        def calcular_lucro(row):
                            nome_prod_formatado = row['Produto'].split(" - ")[1]
                            match = df_prod[df_prod['Produto'] == nome_prod_formatado]
                            if not match.empty:
                                custo = float(match.iloc[0]['Preco compra'])
                                preco_unitario = float(row['Preco total']) / float(row['Quantidade'])
                                return (preco_unitario - custo) * float(row['Quantidade'])
                            return 0
                        
                        df_vendas['Lucro Total'] = df_vendas.apply(calcular_lucro, axis=1)
                        
                        # --- AQUI ESTÁ O AJUSTE: ABRA AS COLUNAS ANTES ---
                        col1, col2, col3 = st.columns(3)
                        
                        # Coluna 1: Total Vendido
                        col1.metric("Total Vendido", f"R$ {df_vendas['Preco total'].sum():,.2f}")
                        
                        # Coluna 2: Lucro Total
                        col2.metric("Lucro Total", f"R$ {df_vendas['Lucro Total'].sum():,.2f}")
                        
                        # Coluna 3: Total de Vendas (Quantidade de pedidos)
                        col3.metric("Nº de Vendas", len(df_vendas))
                        
                        st.divider() # Adiciona uma linha horizontal para organizar
                        
                        st.subheader("Lucro por Cliente")
                        # Mantenha apenas um st.bar_chart (você tinha repetido no código)
                        st.bar_chart(df_vendas.groupby('Cliente')['Lucro Total'].sum())
                        
                    else:
                        st.info("Nenhuma venda registrada.")
                except Exception as e:
                    st.error(f"Erro ao carregar relatório: {e}")
