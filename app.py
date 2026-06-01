import streamlit as st
import pandas as pd

# Título do Projeto
st.title("CRM da Mãe")

# Inicializar a lista de clientes no estado da sessão
if 'clientes' not in st.session_state:
    st.session_state.clientes = []

# --- Formulário de Inserção ---
st.subheader("Adicionar Novo Cliente")
with st.form("form_cliente", clear_on_submit=True):
    nome = st.text_input("Nome do Cliente")
    telefone = st.text_input("Telefone")
    email = st.text_input("E-mail")
    submit_button = st.form_submit_button("Salvar Cliente")

    if submit_button:
        if nome:
            novo_cliente = {"Nome": nome, "Telefone": telefone, "Email": email}
            st.session_state.clientes.append(novo_cliente)
            st.success(f"Cliente {nome} adicionado com sucesso!")
        else:
            st.error("O campo nome é obrigatório.")

# --- Funcionalidade de Listagem ---
st.subheader("Lista de Clientes")
if len(st.session_state.clientes) > 0:
    df = pd.DataFrame(st.session_state.clientes)
    st.table(df)
else:
    st.info("Nenhum cliente cadastrado ainda.")
