import streamlit as st
from utils.database import save_session_data
from modules.achievements import check_and_award_achievement
from api.openai_api import get_assistant_response
import json

def display_kanban_board():
    st.title("Quadro Kanban")
    
    if 'kanban_tasks' not in st.session_state:
        st.session_state['kanban_tasks'] = {'To Do': [], 'In Progress': [], 'Done': []}
    
    kanban_tasks = st.session_state['kanban_tasks']
    
    # Garantir que todas as colunas existam
    for status in ['To Do', 'In Progress', 'Done']:
        if status not in kanban_tasks:
            kanban_tasks[status] = []
    
    # Adicionar nova tarefa
    with st.expander("Adicionar Nova Tarefa", expanded=False):
        col1, col2 = st.columns([3, 1])
        with col1:
            new_task = st.text_input("Descrição da Tarefa", key="new_kanban_task")
        with col2:
            priority = st.selectbox("Prioridade", ["Baixa", "Média", "Alta"], key="new_task_priority")
        if st.button("Adicionar Tarefa", key="add_kanban_task", use_container_width=True):
            if new_task:
                kanban_tasks['To Do'].append({"description": new_task, "priority": priority})
                save_session_data(st.session_state['user'])
                st.success("Tarefa adicionada com sucesso!")
                st.rerun()
            else:
                st.warning("Por favor, digite uma descrição para a tarefa.")

    # Exibir o quadro Kanban
    columns = st.columns(3)
    statuses = ["To Do", "In Progress", "Done"]
    colors = ["#FF9999", "#FFCC99", "#99FF99"]

    for col, status, color in zip(columns, statuses, colors):
        with col:
            st.markdown(f"<h3 style='background-color: {color}; padding: 10px; border-radius: 5px; text-align: center;'>{status}</h3>", unsafe_allow_html=True)
            for i, task in enumerate(kanban_tasks[status]):
                with st.container():
                    priority_color = {"Alta": "red", "Média": "orange", "Baixa": "green"}[task['priority']]
                    st.markdown(f"""
                    <div style='background-color: white; padding: 10px; border-radius: 5px; margin-bottom: 10px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); border-left: 5px solid {priority_color};'>
                        <h4 style='margin: 0;'>{task['description']}</h4>
                        <p style='margin: 5px 0 0 0; font-size: 0.8em; color: {priority_color};'>Prioridade: {task['priority']}</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        if st.button("✏️", key=f"edit_{status}_{i}", help="Editar tarefa"):
                            st.session_state[f'editing_{status}_{i}'] = True
                    with col2:
                        if st.button("🗑️", key=f"delete_{status}_{i}", help="Excluir tarefa"):
                            kanban_tasks[status].pop(i)
                            save_session_data(st.session_state['user'])
                            st.rerun()
                    with col3:
                        move_options = [s for s in statuses if s != status]
                        move_to = st.selectbox("", move_options, key=f"move_{status}_{i}", label_visibility="collapsed")
                        if st.button("➡️", key=f"move_button_{status}_{i}", help="Mover tarefa"):
                            task_to_move = kanban_tasks[status].pop(i)
                            kanban_tasks[move_to].append(task_to_move)
                            save_session_data(st.session_state['user'])
                            st.rerun()
                
                if st.session_state.get(f'editing_{status}_{i}', False):
                    with st.form(key=f"edit_form_{status}_{i}"):
                        new_description = st.text_input("Nova descrição", value=task['description'])
                        new_priority = st.selectbox("Nova prioridade", ["Baixa", "Média", "Alta"], index=["Baixa", "Média", "Alta"].index(task['priority']))
                        col1, col2 = st.columns(2)
                        with col1:
                            if st.form_submit_button("Salvar", use_container_width=True):
                                task['description'] = new_description
                                task['priority'] = new_priority
                                save_session_data(st.session_state['user'])
                                st.session_state[f'editing_{status}_{i}'] = False
                                st.rerun()
                        with col2:
                            if st.form_submit_button("Cancelar", use_container_width=True):
                                st.session_state[f'editing_{status}_{i}'] = False
                                st.rerun()

    check_and_award_achievement("Produtividade", "Utilizou o Kanban para gerenciar tarefas.")

def generate_initial_kanban_tasks(idea, questions, answers):
    prompt = f"""
Com base na seguinte ideia de negócio e nas perguntas e respostas fornecidas, gere 15 tarefas iniciais para um quadro Kanban. As tarefas devem ser relevantes para iniciar e desenvolver o negócio. Inclua uma prioridade para cada tarefa (Alta, Média ou Baixa).

Ideia de Negócio: {idea}

Perguntas e Respostas:
{' '.join([f"P: {q}\nR: {a}\n" for q, a in zip(questions, answers)])}

Forneça a resposta no seguinte formato JSON:

{{
    "tasks": [
        {{"description": "tarefa 1", "priority": "Alta"}},
        {{"description": "tarefa 2", "priority": "Média"}},
        ...
    ]
}}
"""
    
    try:
        response = get_assistant_response([{"role": "user", "content": prompt}])
        if not response:
            raise ValueError("Resposta da API está vazia.")
        tasks_dict = json.loads(response)
        return tasks_dict.get('tasks', [])
    except json.JSONDecodeError:
        st.error("Erro ao decodificar a resposta JSON da API.")
        return []
    except Exception as e:
        st.error(f"Erro ao gerar tarefas iniciais do Kanban: {e}")
        return []

def initialize_kanban(idea, questions, answers):
    initial_tasks = generate_initial_kanban_tasks(idea, questions, answers)
    st.session_state['kanban_tasks'] = {
        'To Do': initial_tasks,
        'In Progress': [],
        'Done': []
    }
    save_session_data(st.session_state['user'])
    st.success("Quadro Kanban inicial gerado com sucesso!")