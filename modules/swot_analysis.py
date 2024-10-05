import streamlit as st
import plotly.graph_objects as go
from utils.database import save_session_data
from modules.achievements import check_and_award_achievement
from api.openai_api import get_assistant_response
import json
import re

def display_swot_analysis():
    st.title("Análise SWOT")
    
    # CSS atualizado
    st.markdown("""
    <style>
    .stButton > button {
        background-color: #e8e8e8 !important;
        color: #000000 !important;
        border: none !important;
        border-radius: 4px !important;
        padding: 0.5rem 1rem !important;
        font-weight: 600 !important;
        width: 100% !important;
    }
    .stButton > button:hover {
        background-color: #73B6E6 !important;
    }
    .stButton > button:focus {
        background-color: #89CFF0 !important;
        box-shadow: none !important;
    }
    div[data-testid="stToolbar"] {
        display: none;
    }
    .full-width-button {
        width: 100%;
        text-align: center;
    }
    .full-width-button button {
        width: 100%;
    }
    </style>
    """, unsafe_allow_html=True)

    # Exibir o quadro SWOT
    columns = st.columns(4)
    categories = ["Forças", "Fraquezas", "Oportunidades", "Ameaças"]
    colors = ["#0066cc", "#0099cc", "#66cc99", "#ff9933"]

    for col, category, color in zip(columns, categories, colors):
        with col:
            st.markdown(f"<h3 style='background-color: {color}; padding: 10px; border-radius: 5px; text-align: center; color: white;'>{category}</h3>", unsafe_allow_html=True)
            
            for i, item in enumerate(st.session_state['swot'][category.lower()]):
                card_key = f"{category}_{i}"
                
                # Card clicável
                if st.button(item, key=f"card_{card_key}", use_container_width=True):
                    st.session_state[f'editing_{card_key}'] = True
                
                # Campos de edição e exclusão
                if st.session_state.get(f'editing_{card_key}', False):
                    with st.form(key=f"edit_form_{card_key}"):
                        new_description = st.text_input("Nova descrição", value=item)
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            if st.form_submit_button("Salvar", use_container_width=True):
                                st.session_state['swot'][category.lower()][i] = new_description
                                save_session_data(st.session_state['user'])
                                st.session_state[f'editing_{card_key}'] = False
                                st.rerun()
                        with col2:
                            if st.form_submit_button("Excluir", use_container_width=True):
                                st.session_state['swot'][category.lower()].pop(i)
                                save_session_data(st.session_state['user'])
                                st.session_state[f'editing_{card_key}'] = False
                                st.rerun()
                        with col3:
                            if st.form_submit_button("Cancelar", use_container_width=True):
                                st.session_state[f'editing_{card_key}'] = False
                                st.rerun()
            
            # Botão para adicionar novo item
            add_key = f"add_{category.lower()}"
            if st.button(f"+ Adicionar {category.lower()}", key=add_key, use_container_width=True):
                st.session_state[f'adding_{add_key}'] = True
            
            # Campo de entrada para novo item
            if st.session_state.get(f'adding_{add_key}', False):
                with st.form(key=f"add_form_{add_key}"):
                    new_item = st.text_input(f"Novo item para {category.lower()}")
                    if st.form_submit_button("Adicionar", use_container_width=True):
                        if new_item:
                            st.session_state['swot'][category.lower()].append(new_item)
                            save_session_data(st.session_state['user'])
                            st.success(f"{category[:-1]} adicionada com sucesso!")
                            st.session_state[f'adding_{add_key}'] = False
                            st.rerun()

    check_and_award_achievement("Análise Estratégica", "Completou a análise SWOT.")

    if st.button("Gerar Gráfico SWOT", use_container_width=True):
        generate_swot_chart()
    if st.session_state.get('swot_graph_data'):
        st.plotly_chart(st.session_state['swot_graph_data'])

def generate_swot_chart():
    strengths = len(st.session_state['swot']['forças'])
    weaknesses = len(st.session_state['swot']['fraquezas'])
    opportunities = len(st.session_state['swot']['oportunidades'])
    threats = len(st.session_state['swot']['ameaças'])

    fig = go.Figure()

    fig.add_trace(go.Barpolar(
        r=[strengths, weaknesses, opportunities, threats],
        theta=['Forças', 'Fraquezas', 'Oportunidades', 'Ameaças'],
        marker_color=['#2ecc71', '#e74c3c', '#3498db', '#e67e22'],
        marker_line_color="black",
        marker_line_width=1,
        opacity=0.8
    ))

    fig.update_layout(
        template=None,
        polar=dict(
            radialaxis=dict(visible=True, range=[0, max(strengths, weaknesses, opportunities, threats) + 1])
        ),
        showlegend=False,
        title="Gráfico SWOT"
    )

    st.session_state['swot_graph_data'] = fig

def generate_swot_analysis(idea):
    prompt = f"""
Com base na seguinte ideia de negócio, realize uma análise SWOT completa. Forneça 3 itens para cada categoria:

Ideia de Negócio: {idea}

Forneça a resposta no seguinte formato JSON:

{{
    "forças": ["força 1", "força 2", "força 3"],
    "fraquezas": ["fraqueza 1", "fraqueza 2", "fraqueza 3"],
    "oportunidades": ["oportunidade 1", "oportunidade 2", "oportunidade 3"],
    "ameaças": ["ameaça 1", "ameaça 2", "ameaça 3"]
}}
"""
    
    try:
        response = get_assistant_response([{"role": "user", "content": prompt}])
        
        # Tenta primeiro fazer o parse do JSON diretamente
        try:
            swot_analysis = json.loads(response)
        except json.JSONDecodeError:
            # Se falhar, tenta extrair o JSON da resposta usando regex
            json_match = re.search(r'\{.*\}', response, re.DOTALL)
            if json_match:
                try:
                    swot_analysis = json.loads(json_match.group())
                except json.JSONDecodeError:
                    raise ValueError("Não foi possível extrair um JSON válido da resposta.")
            else:
                raise ValueError("Não foi possível encontrar um JSON na resposta.")
        
        # Verifica se todas as chaves necessárias estão presentes
        required_keys = ['forças', 'fraquezas', 'oportunidades', 'ameaças']
        if not all(key in swot_analysis for key in required_keys):
            raise ValueError("O JSON não contém todas as categorias SWOT necessárias.")
        
        return swot_analysis
    except Exception as e:
        st.error(f"Erro ao gerar análise SWOT: {e}")
        return {
            "forças": [],
            "fraquezas": [],
            "oportunidades": [],
            "ameaças": []
        }

def update_swot_analysis(swot_data):
    st.session_state['swot'] = swot_data
    save_session_data(st.session_state['user'])
    st.success("Análise SWOT atualizada com sucesso!")