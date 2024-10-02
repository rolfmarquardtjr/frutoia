import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import datetime
from api.openai_api import get_assistant_response
import json
from utils.database import save_session_data

def display_expense_tracker():
    st.title("Controle de Gastos")
    
    st.header("Adicionar Despesa")
    col1, col2, col3 = st.columns(3)
    with col1:
        expense_name = st.text_input("Descrição")
    with col2:
        expense_amount = st.number_input("Valor", min_value=0.0, step=0.01)
    with col3:
        expense_date = st.date_input("Data", value=datetime.date.today())
    
    if st.button("Adicionar Despesa"):
        if expense_name and expense_amount:
            if 'expenses' not in st.session_state:
                st.session_state['expenses'] = []
            st.session_state['expenses'].append({
                'nome': expense_name,
                'valor': expense_amount,
                'data': expense_date.strftime("%Y-%m-%d")
            })
            save_session_data(st.session_state['user'])
            st.success("Despesa adicionada com sucesso!")
        else:
            st.warning("Por favor, preencha todos os campos.")
    
    if 'expenses' in st.session_state and st.session_state['expenses']:
        st.header("Despesas")
        df = pd.DataFrame(st.session_state['expenses'])
        st.dataframe(df)
        
        total_expenses = sum(expense.get('valor', 0) for expense in st.session_state['expenses'])
        st.metric("Total de Despesas", f"R$ {total_expenses:.2f}")
        
        # Gráfico de pizza das despesas
        fig = go.Figure(data=[go.Pie(labels=df['nome'], values=df['valor'], hole=.3)])
        fig.update_layout(title_text="Distribuição das Despesas")
        st.plotly_chart(fig)

        # Análise de gastos
        if st.button("Analisar Gastos"):
            with st.spinner("Analisando gastos..."):
                analysis = analyze_expenses(df)
                st.write(analysis)

def generate_initial_expenses(idea):
    prompt = f"""
Com base na seguinte ideia de negócio, gere uma lista de 5 despesas iniciais prováveis para começar o negócio.

Ideia de Negócio: {idea}

Forneça a resposta no seguinte formato JSON:

{{
    "despesas": [
        {{"nome": "Aluguel", "valor": 2000}},
        {{"nome": "Equipamentos", "valor": 5000}},
        {{"nome": "Marketing inicial", "valor": 1000}},
        {{"nome": "Licenças e permissões", "valor": 500}},
        {{"nome": "Estoque inicial", "valor": 3000}}
    ]
}}
"""
    
    try:
        response = get_assistant_response([{"role": "user", "content": prompt}])
        expenses_data = json.loads(response)
        expenses = expenses_data['despesas']
        for expense in expenses:
            expense['data'] = datetime.date.today().strftime("%Y-%m-%d")
        st.session_state['expenses'] = expenses
        save_session_data(st.session_state['user'])
        return expenses
    except Exception as e:
        st.error(f"Erro ao gerar despesas iniciais: {e}")
        return []

def analyze_expenses(df):
    try:
        top_expense = df.loc[df['valor'].idxmax()]
        category_totals = df.groupby('nome')['valor'].sum()
        analysis = f"Sua maior despesa é com {top_expense['nome']} no valor de R$ {top_expense['valor']:.2f}.\n"
        analysis += "Resumo das despesas por categoria:\n"
        for name, amount in category_totals.items():
            analysis += f"- {name}: R$ {amount:.2f}\n"
        return analysis
    except Exception as e:
        return f"Erro na análise: {e}"  