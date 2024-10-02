import streamlit as st
import plotly.graph_objects as go
from utils.database import save_session_data
from modules.achievements import check_and_award_achievement
from api.openai_api import get_assistant_response
import json
import re

def display_swot_analysis():
    st.title("Análise SWOT")
    
    categories = ['forças', 'fraquezas', 'oportunidades', 'ameaças']
    for category in categories:
        st.header(category.capitalize())
        new_item = st.text_input(f"Adicionar {category}", key=f"add_{category}")
        if st.button(f"Adicionar {category}", key=f"add_button_{category}"):
            if new_item:
                st.session_state['swot'][category].append(new_item)
                save_session_data(st.session_state['user'])
                st.success(f"{category.capitalize()} adicionada com sucesso!")
        if st.session_state['swot'][category]:
            st.write(f"**{category.capitalize()}:**")
            for item in st.session_state['swot'][category]:
                st.write(f"- {item}")
        else:
            st.write(f"Sem {category} adicionadas ainda.")
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
        swot_analysis = eval(response)  # Convert string to dictionary
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