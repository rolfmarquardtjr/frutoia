import streamlit as st
from config import initialize_session_state
from modules.authentication import login, register
from modules.dashboard import display_dashboard, generate_and_store_dashboard
from modules.swot_analysis import display_swot_analysis, generate_swot_analysis, update_swot_analysis
from modules.financial_projections import display_financial_projections, generate_initial_financial_projections
from modules.ai_assistant import display_ai_assistant
from modules.expense_tracker import display_expense_tracker, generate_initial_expenses
from modules.kanban_board import display_kanban_board, initialize_kanban
from modules.goals import display_goals
from modules.networking import display_networking
from modules.market_research import display_market_research
from modules.legal_consultant import display_legal_consultant
from modules.achievements import display_achievements, check_and_award_achievement, calculate_progress
from utils.pdf_generator import export_to_pdf
from ui.styles import load_css
from ui.components import render_menu
from api.openai_api import generate_questions_with_openai

st.set_page_config(layout="wide", page_title="fruto.ia", page_icon="💼")

st.markdown("""
    <style>
    input[type="text"], input[type="number"], textarea {
        background-color: white !important;
    }
    .center-content {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        text-align: center;
    }
    </style>
    """, unsafe_allow_html=True)

def main():
    load_css()
    initialize_session_state()

    if 'user' not in st.session_state:
        tab1, tab2 = st.tabs(["Login", "Registro"])
        with tab1:
            login()
        with tab2:
            register()
    else:
        # Inicializando listas no session_state
        if 'swot' not in st.session_state:
            st.session_state['swot'] = {
                'forças': [],
                'fraquezas': [],
                'oportunidades': [],
                'ameaças': []
            }

        page = render_menu()

        if page == "Início":
            display_home()
        elif page == "Dashboard":
            display_dashboard()
        elif page == "Análise SWOT":
            display_swot_analysis()
        elif page == "Projeções Financeiras":
            display_financial_projections()
        elif page == "Assistente IA":
            display_ai_assistant()
        elif page == "Controle de Gastos":
            display_expense_tracker()
        elif page == "Kanban":
            display_kanban_board()
        elif page == "Metas":
            display_goals()
        elif page == "Rede de Networking":
            display_networking()
        elif page == "Conquistas":
            display_achievements()
        elif page == "Pesquisa de Mercado":
            display_market_research()
        elif page == "Consultor Jurídico":
            display_legal_consultant()

def display_home():
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("""
            <div style='text-align: center;'>
                <h1>Bem-vindo ao Fruto.IA</h1>
                <p>Descreva sua ideia de negócio e nós ajudaremos você a desenvolver um plano!</p>
            </div>
        """, unsafe_allow_html=True)

    # Barra de progresso padrão
    st.header("Seu Progresso")
    progress = calculate_progress()
    st.session_state['progress'] = progress
    st.progress(progress / 100)

    if 'business_generated' not in st.session_state:
        st.session_state['business_generated'] = False

    if 'questions_generated' not in st.session_state:
        st.session_state['questions_generated'] = False

    if not st.session_state['business_generated']:
        # Passo 1: Ideia de Negócio
        st.header("Passo 1: Descreva sua ideia de negócio")
        user_idea = st.text_area("Descreva sua ideia de negócio", value=st.session_state.get('user_idea', ''))
        if st.button("Gerar Perguntas", key="generate_questions"):
            if user_idea:
                st.session_state['user_idea'] = user_idea
                with st.spinner('Gerando perguntas...'):
                    questions = generate_questions(user_idea)
                    if questions:
                        st.session_state['questions'] = questions
                        st.session_state['questions_generated'] = True
                        st.success('Perguntas geradas com sucesso!')
                        check_and_award_achievement("Primeiros Passos", "Descreveu a ideia de negócio.")
                    else:
                        st.error("Não foi possível gerar perguntas. Por favor, tente novamente.")
            else:
                st.warning("Por favor, descreva sua ideia de negócio.")
    else:
        st.info("Você já gerou um plano de negócios. Clique em 'Gerar Novo Negócio' para começar um novo.")

    # Passo 2: Responder Perguntas
    if st.session_state.get('questions_generated') and not st.session_state['business_generated']:
        st.header("Passo 2: Responda às seguintes perguntas")
        answers = []
        for i, question in enumerate(st.session_state['questions']):
            answer = st.text_input(f"{i+1}. {question}", key=f"answer_{i}")
            answers.append(answer)
        
        st.session_state['answers'] = answers

        if st.button('Gerar Resultados', key="generate_results"):
            with st.spinner("Gerando resultados..."):
                try:
                    # Gerar Dashboard
                    generate_and_store_dashboard()

                    # Gerar Análise SWOT
                    swot = generate_swot_analysis(st.session_state['user_idea'])
                    st.session_state['swot'] = swot

                    # Gerar Kanban
                    initialize_kanban(st.session_state['user_idea'], st.session_state['questions'], st.session_state['answers'])

                    # Gerar Projeções Financeiras iniciais
                    generate_initial_financial_projections(st.session_state['user_idea'])

                    # Gerar Despesas iniciais
                    generate_initial_expenses(st.session_state['user_idea'])

                    st.session_state['business_generated'] = True
                    st.success("Todos os resultados foram gerados com sucesso! Explore as diferentes seções para ver os detalhes.")
                except Exception as e:
                    st.error(f"Erro ao gerar resultados: {str(e)}")
                    st.error("Por favor, tente novamente. Se o problema persistir, entre em contato com o suporte.")

    if st.session_state['business_generated']:
        if st.button('Gerar Novo Negócio', key="generate_new_business"):
            st.session_state['business_generated'] = False
            st.session_state['questions_generated'] = False
            st.session_state['user_idea'] = ''
            st.session_state['questions'] = []
            st.session_state['answers'] = []
            st.session_state['swot'] = {
                'forças': [],
                'fraquezas': [],
                'oportunidades': [],
                'ameaças': []
            }
            st.success("Você pode começar um novo negócio agora!")
            st.rerun()

def generate_questions(idea):
    try:
        questions = generate_questions_with_openai(idea)
        if not questions:
            st.error("A API não retornou perguntas. Por favor, tente novamente.")
            return []
        return questions
    except Exception as e:
        st.error(f'Erro ao gerar perguntas: {e}')
        return []

if __name__ == '__main__':
    main()