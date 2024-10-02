import streamlit as st
from utils.database import create_user, check_user, load_session_data

def login():
    st.title("Login")
    username = st.text_input("Nome de usuário", key="login_username")
    password = st.text_input("Senha", type="password", key="login_password")
    if st.button("Login", key="login_button"):
        if check_user(username, password):
            st.session_state['user'] = username
            session_data = load_session_data(username)
            if session_data:
                st.session_state.update(session_data)
            st.success("Login bem-sucedido!")
            st.rerun()
        else:
            st.error("Nome de usuário ou senha incorretos")

def register():
    st.title("Registro")
    username = st.text_input("Nome de usuário", key="register_username")
    password = st.text_input("Senha", type="password", key="register_password")
    if st.button("Registrar", key="register_button"):
        if create_user(username, password):
            st.success("Usuário registrado com sucesso! Faça login para continuar.")
        else:
            st.error("Nome de usuário já existe")