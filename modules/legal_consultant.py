import streamlit as st
from api.openai_api import generate_legal_plan
from utils.database import save_session_data
from modules.achievements import check_and_award_achievement

def display_legal_consultant():
    st.title("Consultor Jurídico IA")
    
    st.write("Obtenha orientações gerais sobre como iniciar seu negócio legalmente.")
    if st.button("Gerar Plano Jurídico"):
        with st.spinner("Analisando requisitos legais..."):
            legal_plan = generate_legal_plan(st.session_state['user_idea'])
            st.session_state['legal_plan'] = legal_plan
            save_session_data(st.session_state['user'])
            st.success("Plano jurídico gerado com sucesso!")
            check_and_award_achievement("Conformidade Legal", "Obteve plano de ação legal.")
    
    if st.session_state.get('legal_plan'):
        st.header("Plano de Ação Jurídico")
        st.write(st.session_state['legal_plan'])