import streamlit as st
import pandas as pd
import plotly.express as px

# --- CONFIGURAÇÃO VISUAL ---
st.set_page_config(page_title="Boutique de Perfumes", layout="wide")

# CSS para o estilo "Boutique" e Mobile
st.markdown("""
    <style>
    .stApp {background-image: url('https://img.freepik.com/fotos-gratis/fundo-rosa-pastel-com-textura_23-2148785900.jpg'); background-size: cover;}
    .produto-card {background: rgba(255, 255, 255, 0.9); padding: 15px; border-radius: 20px; border: 1px solid #d4af37; margin-bottom: 15px;}
    h1 {color: #8a2be2; text-align: center;}
    </style>
""", unsafe_allow_html=True)

# Carregar Dados
sheet_id = "1-NQNbRKtOeLtw47ThMkobuEwYN8TvFRcvVWgvst_-M0"
url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet=Sheet1"
df = pd.read_csv(url)
df.columns = df.columns.str.strip()

# --- ÁREA ADMINISTRATIVA ---
with st.sidebar:
    st.subheader("🔐 Área da Gerente")
    senha = st.text_input("Senha da Gerente", type="password")

# --- CONTEÚDO PRINCIPAL ---
st.title("✨ Boutique de Perfumes")

# Abas
aba1, aba3 = st.tabs(["🛍️ Catálogo", "👤 Cadastro"])

with aba1:
    genero = st.selectbox("Filtrar por:", ["Todos", "Masculino", "Feminino"])
    df_f = df if genero == "Todos" else df[df['Categoria'] == genero]
    
    for idx, row in df_f.iterrows():
        with st.container():
            st.markdown('<div class="produto-card">', unsafe_allow_html=True)
            st.subheader(f"{row['Produto']}")
            c1, c2 = st.columns(2)
            c1.write(f"Preço: R$ {row['Preço Venda']:.2f}")
            qtd = c2.number_input("Qtd", 1, int(row['Estoque']), key=f"q{idx}")
            
            if st.button("🛒 Comprar", key=f"btn{idx}"):
                msg = f"Olá, quero {qtd}x {row['Produto']}!"
                st.link_button("Enviar no WhatsApp", f"https://wa.me/5551993144399?text={msg.replace(' ', '%20')}")
            st.markdown('</div>', unsafe_allow_html=True)

# --- DASHBOARD PROTEGIDO ---
if senha == "1234": # Troque a senha aqui!
    with st.expander("📊 Painel Financeiro (Privado)"):
        st.metric("Lucro Total", f"R$ {(df['Preço Venda'] - df['Preço Pago']).sum():.2f}")
        fig = px.bar(df, x='Produto', y=df['Preço Venda'] - df['Preço Pago'], title="Lucro por item")
        st.plotly_chart(fig)

with aba3:
    with st.form("cadastro"):
        st.text_input("Nome")
        st.text_input("CPF")
        if st.form_submit_button("Cadastrar"):
            st.success("Cadastro realizado!")
