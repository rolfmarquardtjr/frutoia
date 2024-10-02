import streamlit as st
import plotly.graph_objects as go
from utils.database import save_session_data
from modules.achievements import check_and_award_achievement
from api.openai_api import get_assistant_response
import json
import re

def display_swot_analysis():
    st.title("Análise SWOT")
    
    # Container da análise SWOT
    st.markdown("<div class='swot-container'>", unsafe_allow_html=True)

    # Forças
    st.markdown("<div class='swot-item forcas'>", unsafe_allow_html=True)
    st.markdown("<div class='swot-icon'><img src='https://cdn-icons-png.flaticon.com/512/190/190411.png' width='50'/></div>", unsafe_allow_html=True)
    st.header("Forças")
    add_strength = st.text_input("Adicionar forças", key="add_strength")
    if st.button("Adicionar forças", key="add_strength_button"):
        if add_strength:
            st.session_state['swot']['forças'].append(add_strength)
            save_session_data(st.session_state['user'])
            st.success("Força adicionada com sucesso!")
    st.markdown("**Forças:**")
    st.markdown("<ul>", unsafe_allow_html=True)
    for strength in st.session_state['swot']['forças']:
        st.markdown(f"<li>{strength}</li>", unsafe_allow_html=True)
    st.markdown("</ul>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # Fraquezas
    st.markdown("<div class='swot-item fraquezas'>", unsafe_allow_html=True)
    st.markdown("<div class='swot-icon'><img src='https://cdn-icons-png.flaticon.com/512/190/190406.png' width='50'/></div>", unsafe_allow_html=True)
    st.header("Fraquezas")
    add_weakness = st.text_input("Adicionar fraquezas", key="add_weakness")
    if st.button("Adicionar fraquezas", key="add_weakness_button"):
        if add_weakness:
            st.session_state['swot']['fraquezas'].append(add_weakness)
            save_session_data(st.session_state['user'])
            st.success("Fraqueza adicionada com sucesso!")
    st.markdown("**Fraquezas:**")
    st.markdown("<ul>", unsafe_allow_html=True)
    for weakness in st.session_state['swot']['fraquezas']:
        st.markdown(f"<li>{weakness}</li>", unsafe_allow_html=True)
    st.markdown("</ul>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # Oportunidades
    st.markdown("<div class='swot-item oportunidades'>", unsafe_allow_html=True)
    st.markdown("<div class='swot-icon'><img src='https://cdn-icons-png.flaticon.com/512/190/190407.png' width='50'/></div>", unsafe_allow_html=True)
    st.header("Oportunidades")
    add_opportunity = st.text_input("Adicionar oportunidades", key="add_opportunity")
    if st.button("Adicionar oportunidades", key="add_opportunity_button"):
        if add_opportunity:
            st.session_state['swot']['oportunidades'].append(add_opportunity)
            save_session_data(st.session_state['user'])
            st.success("Oportunidade adicionada com sucesso!")
    st.markdown("**Oportunidades:**")
    st.markdown("<ul>", unsafe_allow_html=True)
    for opportunity in st.session_state['swot']['oportunidades']:
        st.markdown(f"<li>{opportunity}</li>", unsafe_allow_html=True)
    st.markdown("</ul>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # Ameaças
    st.markdown("<div class='swot-item ameacas'>", unsafe_allow_html=True)
    st.markdown("<div class='swot-icon'><img src='https://cdn-icons-png.flaticon.com/512/190/190408.png' width='50'/></div>", unsafe_allow_html=True)
    st.header("Ameaças")
    add_threat = st.text_input("Adicionar ameaças", key="add_threat")
    if st.button("Adicionar ameaças", key="add_threat_button"):
        if add_threat:
            st.session_state['swot']['ameaças'].append(add_threat)
            save_session_data(st.session_state['user'])
            st.success("Ameaça adicionada com sucesso!")
    st.markdown("**Ameaças:**")
    st.markdown("<ul>", unsafe_allow_html=True)
    for threat in st.session_state['swot']['ameaças']:
        st.markdown(f"<li>{threat}</li>", unsafe_allow_html=True)
    st.markdown("</ul>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

    check_and_award_achievement("Análise Estratégica", "Completou a análise SWOT.")

    if st.button("Gerar Gráfico SWOT"):
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