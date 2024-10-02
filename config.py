import os
from dotenv import load_dotenv
from openai import OpenAI
import streamlit as st

# Carregar variáveis de ambiente
load_dotenv()

# Inicializar o cliente da API OpenAI
client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
)

def initialize_session_state():
    if 'swot' not in st.session_state:
        st.session_state['swot'] = {
            'forças': [],
            'fraquezas': [],
            'oportunidades': [],
            'ameaças': []
        }
    if 'completed_tasks' not in st.session_state:
        st.session_state['completed_tasks'] = set()
    if 'action_plans' not in st.session_state:
        st.session_state['action_plans'] = {}
    if 'user_idea' not in st.session_state:
        st.session_state['user_idea'] = ''
    if 'questions' not in st.session_state:
        st.session_state['questions'] = []
    if 'expenses' not in st.session_state:
        st.session_state['expenses'] = []
    if 'goals' not in st.session_state:
        st.session_state['goals'] = []
    if 'kanban_tasks' not in st.session_state:
        st.session_state['kanban_tasks'] = {
            'To Do': [],
            'In Progress': [],
            'Done': []
        }
    if 'achievements' not in st.session_state:
        st.session_state['achievements'] = []
    if 'progress' not in st.session_state:
        st.session_state['progress'] = 0
    if 'show_tutorial' not in st.session_state:
        st.session_state['show_tutorial'] = True
    if 'search_results' not in st.session_state:
        st.session_state['search_results'] = []
    if 'personalized_tips' not in st.session_state:
        st.session_state['personalized_tips'] = []
    if 'legal_advice' not in st.session_state:
        st.session_state['legal_advice'] = ''
    if 'legal_plan' not in st.session_state:
        st.session_state['legal_plan'] = ''
    if 'swot_graph_data' not in st.session_state:
        st.session_state['swot_graph_data'] = None