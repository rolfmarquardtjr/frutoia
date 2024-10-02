import streamlit as st
import uuid
from utils.database import save_session_data
from modules.achievements import check_and_award_achievement

def display_goals():
    st.title("Metas")
    
    st.header("Adicionar Meta")
    goal_name = st.text_input("Descrição da Meta")
    goal_deadline = st.date_input("Prazo")
    
    if st.button("Adicionar Meta"):
        if goal_name and goal_deadline:
            st.session_state['goals'].append({
                'name': goal_name,
                'deadline': goal_deadline,
                'completed': False
            })
            save_session_data(st.session_state['user'])
            st.success("Meta adicionada com sucesso!")
            check_and_award_achievement("Objetivos Definidos", "Criou uma nova meta.")
        else:
            st.warning("Por favor, preencha todos os campos.")
    
    if st.session_state['goals']:
        st.header("Suas Metas")
        for goal in st.session_state['goals']:
            col1, col2, col3 = st.columns([3,2,1])
            with col1:
                st.write(goal['name'])
            with col2:
                st.write(f"Prazo: {goal['deadline']}")
            with col3:
                if st.checkbox("Concluída", value=goal['completed'], key=uuid.uuid4()):
                    goal['completed'] = True
                else:
                    goal['completed'] = False
        save_session_data(st.session_state['user'])