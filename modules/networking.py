import streamlit as st
from api.openai_api import generate_networking_suggestions
from modules.achievements import check_and_award_achievement

def display_networking():
    st.title("Rede de Networking")
    
    st.write("Com base na sua ideia de negócio, aqui estão algumas sugestões de eventos e recursos para você:")
    suggestions = get_networking_suggestions(st.session_state['user_idea'])
    if suggestions:
        for suggestion in suggestions:
            st.write(f"- {suggestion}")
    check_and_award_achievement("Conexões", "Explorou a rede de networking.")

def get_networking_suggestions(idea):
    try:
        suggestions = generate_networking_suggestions(idea)
        return suggestions
    except Exception as e:
        st.error(f'Erro ao obter sugestões: {e}')
        return []