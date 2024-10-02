import streamlit as st
from api.google_api import search_internet
from utils.database import save_session_data
from modules.achievements import check_and_award_achievement

def display_market_research():
    st.title("Pesquisa de Mercado")
    
    st.header("Pesquise sobre um tópico específico")
    query = st.text_input("Digite o tópico que deseja pesquisar")
    if st.button("Pesquisar"):
        if query:
            with st.spinner("Realizando pesquisa..."):
                results = perform_market_research(query)
                st.session_state['search_results'] = results
                save_session_data(st.session_state['user'])
                st.success("Pesquisa concluída!")
        else:
            st.warning("Por favor, digite um tópico para pesquisar.")
    
    if st.session_state['search_results']:
        st.header("Resultados da Pesquisa")
        for result in st.session_state['search_results']:
            st.write(f"- {result}")
        check_and_award_achievement("Pesquisador", "Realizou uma pesquisa de mercado.")

def perform_market_research(query):
    try:
        result = search_internet(query)
        return result.split('\n')
    except Exception as e:
        st.error(f"Erro ao realizar a pesquisa: {e}")
        return []