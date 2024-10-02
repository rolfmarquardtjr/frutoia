import sqlite3
import hashlib
import pickle
import streamlit as st

# Configuração do banco de dados SQLite
conn = sqlite3.connect('data/user_data.db', check_same_thread=False)
c = conn.cursor()

# Criar tabela de usuários se não existir
c.execute('''CREATE TABLE IF NOT EXISTS users
             (username TEXT PRIMARY KEY, password TEXT, session_data BLOB)''')
conn.commit()

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def create_user(username, password):
    hashed_password = hash_password(password)
    try:
        c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed_password))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False

def check_user(username, password):
    hashed_password = hash_password(password)
    c.execute("SELECT * FROM users WHERE username=? AND password=?", (username, hashed_password))
    user = c.fetchone()
    return user is not None

def save_session_data(username):
    session_data = pickle.dumps(dict(st.session_state))
    c.execute("UPDATE users SET session_data=? WHERE username=?", (session_data, username))
    conn.commit()

def load_session_data(username):
    c.execute("SELECT session_data FROM users WHERE username=?", (username,))
    result = c.fetchone()
    if result and result[0]:
        return pickle.loads(result[0])
    return {}

def close_connection():
    conn.close()

# Função para ser chamada quando a aplicação for encerrada
import atexit
atexit.register(close_connection)