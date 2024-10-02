import streamlit as st
from streamlit_option_menu import option_menu
from utils.pdf_generator import export_to_pdf

def render_menu():
    with st.sidebar:
        # Renderizando a imagem do logo
        st.image("logo.png", use_column_width=True)
        
        # Renderizando a saudação
        st.markdown(f"<h1 style='color: #1f6391; text-align: center;'>Bora lá, {st.session_state['user']}!</h1>", unsafe_allow_html=True)
        
        # Definindo o menu
        selected = option_menu(
            menu_title=None,  # Sem título adicional
            options=["Início", "Dashboard", "Análise SWOT", "Projeções Financeiras", "Assistente IA", "Controle de Gastos", "Kanban", "Metas", "Rede de Networking", "Conquistas", "Pesquisa de Mercado", "Consultor Jurídico", "Exportar Relatório", "Logout"],  # required
            icons=["house", "bar-chart", "clipboard-data", "currency-dollar", "robot", "wallet", "kanban", "bullseye", "people", "trophy", "search", "briefcase", "file-earmark-arrow-down", "box-arrow-right"],  # optional
            menu_icon="cast",  # optional
            default_index=0,  # optional
            styles={
                "container": {"padding": "5px", "background-color": "#2c3e50"},
                "icon": {"color": "white", "font-size": "25px"},
                "nav-link": {
                    "font-size": "16px",
                    "text-align": "left",
                    "margin": "0px",
                    "color": "white",
                },
                "nav-link-selected": {"background-color": "#1f6391"},
            },
        )
        
        if selected == "Logout":
            st.session_state.clear()
            st.rerun()
        
        if selected == "Exportar Relatório":
            export_to_pdf()
        
        return selected
