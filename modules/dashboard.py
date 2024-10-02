import streamlit as st
import json
from api.openai_api import get_assistant_response
from utils.database import save_session_data
from modules.achievements import check_and_award_achievement

def display_dashboard():
    st.title("Dashboard")
    
    if 'dashboard_data' not in st.session_state or not st.session_state['dashboard_data']:
        st.warning("O dashboard ainda não foi gerado. Por favor, volte à página inicial e gere os resultados.")
        return
    
    data = st.session_state['dashboard_data']
    st.header(data['visao_geral']['nome'])
    st.write(f"**Descrição:** {data['visao_geral']['descricao']}")
    st.write(f"**Modelo de Negócio:** {data['visao_geral']['modelo_negocio']}")
    
    st.subheader("Métricas")
    metrics = data.get('metricas', [])
    num_metrics = len(metrics)
    cols = st.columns(num_metrics)
    for i, metrica in enumerate(metrics):
        with cols[i]:
            st.metric(metrica['nome'], metrica['valor'])
    
    st.subheader("Planos de Ação")
    etapas = data.get('etapas', [])
    for etapa_idx, etapa in enumerate(etapas):
        with st.expander(f"{etapa['titulo']}"):
            st.write(f"**Descrição:** {etapa.get('descricao', 'Não fornecida')}")
            st.write("**Tarefas:**")
            for tarefa_idx, tarefa in enumerate(etapa['tarefas']):
                task_key = f"task_{etapa_idx}_{tarefa_idx}"
                is_completed = st.session_state.get(task_key, False)
                completed = st.checkbox(tarefa, value=is_completed, key=task_key)
                if completed != is_completed:
                    st.session_state[task_key] = completed
                    save_session_data(st.session_state['user'])
            
            if st.button(f"Gerar Plano de Ação para: {etapa['titulo']}", key=f"gen_plan_{etapa_idx}"):
                with st.spinner("Gerando plano de ação detalhado..."):
                    detailed_plan = generate_detailed_action_plan(etapa['titulo'], etapa['tarefas'])
                    st.session_state[f'detailed_plan_{etapa_idx}'] = detailed_plan
            
            if f'detailed_plan_{etapa_idx}' in st.session_state:
                st.markdown(st.session_state[f'detailed_plan_{etapa_idx}'])
    
    st.subheader("Dicas")
    for dica in data.get('dicas', []):
        st.write(f"- {dica}")

def generate_and_store_dashboard():
    st.write("Gerando dashboard...")
    
    idea = st.session_state.get('user_idea', '')
    questions = st.session_state.get('questions', [])
    answers = st.session_state.get('answers', [])
    
    if not idea or not questions or not answers:
        st.error("Informações insuficientes para gerar o dashboard. Certifique-se de ter inserido uma ideia de negócio e respondido às perguntas.")
        return

    prompt = f"""
Com base na seguinte ideia de negócio e nas respostas fornecidas, crie um painel de controle interativo para ajudar o empreendedor a iniciar seu negócio usando o formato JSON a seguir:

{{
    "visao_geral": {{
        "nome": "",
        "descricao": "",
        "modelo_negocio": ""
    }},
    "metricas": [
        {{"nome": "", "valor": ""}},
        {{"nome": "", "valor": ""}},
        {{"nome": "", "valor": ""}},
        {{"nome": "", "valor": ""}}  
    ],
    "etapas": [
        {{
            "titulo": "",
            "descricao": "",
            "tarefas": ["", "", "", ""]
        }},
        {{
            "titulo": "",
            "descricao": "",
            "tarefas": ["", "", "", ""]   
        }}
    ], 
    "dicas": ["", "", "", "", ""]
}}

Ideia: {idea}

Perguntas e Respostas:
{''.join([f"P: {q}\nR: {a}\n" for q, a in zip(questions, answers)])}

Forneça apenas o JSON do Dashboard, sem nenhum texto adicional antes ou depois.
"""
    try:
        response = get_assistant_response([{"role": "system", "content": "Você é um consultor de negócios experiente."}, {"role": "user", "content": prompt}])
        dashboard_data = json.loads(response)
        st.session_state['dashboard_data'] = dashboard_data
        save_session_data(st.session_state['user'])
        st.success('Dashboard gerado com sucesso!')
        check_and_award_achievement("Visão Geral", "Gerou o dashboard do negócio.")
    except json.JSONDecodeError:
        st.error("Erro ao processar a resposta da IA. Por favor, tente novamente.")
    except Exception as e:
        st.error(f'Erro ao gerar dashboard: {e}')

def generate_detailed_action_plan(title, tasks):
    prompt = f"""
Crie um plano de ação detalhado para a seguinte etapa de um negócio:

Etapa: {title}
Tarefas:
{''.join([f"- {task}\n" for task in tasks])}

Forneça um plano de ação detalhado com passos específicos para cada tarefa, incluindo prazos estimados e recursos necessários.
"""
    try:
        response = get_assistant_response([{"role": "system", "content": "Você é um consultor de negócios experiente."}, {"role": "user", "content": prompt}])
        return response
    except Exception as e:
        st.error(f'Erro ao gerar plano de ação detalhado: {e}')
        return "Não foi possível gerar o plano de ação detalhado. Por favor, tente novamente."