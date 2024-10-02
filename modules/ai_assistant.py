import streamlit as st
import json
from api.openai_api import get_assistant_response
from api.google_api import search_internet
from modules.achievements import check_and_award_achievement
from utils.database import save_session_data

def display_ai_assistant():
    st.title("Assistente Virtual IA")
    
    if 'messages' not in st.session_state:
        st.session_state['messages'] = []
    
    for message in st.session_state['messages']:
        if message['role'] == 'user':
            st.write(f"**Você:** {message['content']}")
        elif message['role'] == 'assistant':
            st.write(f"**Assistente:** {message['content']}")
        elif message['role'] == 'function':
            st.write(f"**Função ({message['name']}):** {message['content']}")
    
    user_input = st.text_input("Você:", key="ai_assistant_input")
    if st.button("Enviar", key="ai_assistant_send_button"):
        if user_input:
            st.session_state['messages'].append({'role': 'user', 'content': user_input})
            with st.spinner("Assistente está digitando..."):
                assistant_response = get_assistant_response(st.session_state['messages'])
                if assistant_response:
                    st.session_state['messages'].append({'role': 'assistant', 'content': assistant_response})
                    save_session_data(st.session_state['user'])
                    check_and_award_achievement("Interação com IA", "Utilizou o assistente virtual.")
                else:
                    st.error("Falha ao obter resposta do assistente.")
        else:
            st.warning("Digite uma mensagem para o assistente.")

def get_market_analysis(industry):
    # Aqui você pode implementar lógica real para obter dados do mercado
    sample_data = {
        "tecnologia": "O mercado de tecnologia está crescendo 10% ao ano.",
        "alimentação": "O setor de alimentação saudável está em alta demanda."
    }
    return sample_data.get(industry.lower(), f"Dados atuais do mercado para o setor {industry} não estão disponíveis.")