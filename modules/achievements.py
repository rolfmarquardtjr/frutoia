import streamlit as st
from utils.database import save_session_data

def check_and_award_achievement(title, description):
    if title not in [ach['title'] for ach in st.session_state['achievements']]:
        st.session_state['achievements'].append({'title': title, 'description': description})
        save_session_data(st.session_state['user'])
        st.balloons()
        st.success(f"Conquista desbloqueada: {title}!")

def display_achievements():
    st.title("Conquistas")
    if st.session_state['achievements']:
        for ach in st.session_state['achievements']:
            st.markdown(f"""
            <div style="background-color: #f0f2f6; padding: 10px; border-radius: 5px; margin-bottom: 10px;">
                <h3 style="margin: 0;">🏆 {ach['title']}</h3>
                <p style="margin: 5px 0 0 0;">{ach['description']}</p>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.write("Nenhuma conquista desbloqueada ainda. Continue progredindo!")

def calculate_progress():
    progress = 0
    
    # Verifica se o usuário descreveu a ideia de negócio
    if 'user_idea' in st.session_state and st.session_state['user_idea']:
        progress += 20

    # Verifica se as perguntas foram geradas
    if 'questions_generated' in st.session_state and st.session_state['questions_generated']:
        progress += 20

    # Verifica se as respostas foram fornecidas
    if 'answers' in st.session_state and all(st.session_state['answers']):
        progress += 20

    # Verifica se o plano de negócios foi gerado
    if 'business_generated' in st.session_state and st.session_state['business_generated']:
        progress += 20

    # Verifica se há tarefas concluídas no Kanban
    if 'kanban_tasks' in st.session_state:
        kanban_tasks = st.session_state['kanban_tasks']
        if 'Done' in kanban_tasks and kanban_tasks['Done']:
            progress += 20
        elif any(kanban_tasks.get(status, []) for status in ['To Do', 'In Progress']):
            progress += 10

    return progress