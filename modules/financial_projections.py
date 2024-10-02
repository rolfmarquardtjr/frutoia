import streamlit as st
from api.openai_api import get_assistant_response
import json
from utils.database import save_session_data

def generate_initial_financial_projections(idea):
    prompt = f"""
Com base na seguinte ideia de negócio, gere projeções financeiras iniciais para os próximos 3 anos. Inclua receitas, despesas e lucro/prejuízo projetados.

Ideia de Negócio: {idea}

Forneça a resposta no seguinte formato JSON:

{{
    "ano1": {{
        "receitas": 0,
        "despesas": 0,
        "lucro_prejuizo": 0
    }},
    "ano2": {{
        "receitas": 0,
        "despesas": 0,
        "lucro_prejuizo": 0
    }},
    "ano3": {{
        "receitas": 0,
        "despesas": 0,
        "lucro_prejuizo": 0
    }}
}}

Substitua os valores 0 por estimativas realistas baseadas na ideia de negócio.
"""
    
    try:
        response = get_assistant_response([{"role": "user", "content": prompt}])
        if not response or not response.strip():
            raise ValueError("Resposta da API está vazia.")
        
        # Tenta encontrar o JSON na resposta
        json_start = response.find('{')
        json_end = response.rfind('}') + 1
        if json_start == -1 or json_end == 0:
            raise ValueError("Não foi possível encontrar um JSON válido na resposta.")
        
        json_str = response[json_start:json_end]
        
        # Tenta analisar a resposta como JSON
        financial_projections = json.loads(json_str)
        
        # Verifica se a estrutura do JSON está correta
        for year in ["ano1", "ano2", "ano3"]:
            if year not in financial_projections or not all(key in financial_projections[year] for key in ["receitas", "despesas", "lucro_prejuizo"]):
                raise ValueError("Estrutura JSON inválida na resposta.")
        
        st.session_state['financial_projections'] = financial_projections
        save_session_data(st.session_state['user'])
        st.success("Projeções financeiras iniciais geradas com sucesso!")
    except json.JSONDecodeError as e:
        st.error(f"Erro ao decodificar a resposta JSON da API: {e}")
        st.error(f"Resposta recebida: {response}")
        st.session_state['financial_projections'] = generate_default_projections()
    except Exception as e:
        st.error(f"Erro ao gerar projeções financeiras iniciais: {e}")
        st.error(f"Resposta recebida: {response}")
        st.session_state['financial_projections'] = generate_default_projections()

def generate_default_projections():
    return {
        "ano1": {"receitas": 100000, "despesas": 80000, "lucro_prejuizo": 20000},
        "ano2": {"receitas": 150000, "despesas": 100000, "lucro_prejuizo": 50000},
        "ano3": {"receitas": 200000, "despesas": 120000, "lucro_prejuizo": 80000}
    }

def display_financial_projections():
    st.title("Projeções Financeiras")
    
    if 'financial_projections' not in st.session_state:
        st.warning("Nenhuma projeção financeira gerada ainda. Por favor, gere uma ideia de negócio primeiro.")
        return
    
    projections = st.session_state['financial_projections']
    
    for year, data in projections.items():
        st.subheader(f"Projeções para {year}")
        col1, col2, col3 = st.columns(3)
        col1.metric("Receitas", f"R$ {data['receitas']:,.2f}")
        col2.metric("Despesas", f"R$ {data['despesas']:,.2f}")
        col3.metric("Lucro/Prejuízo", f"R$ {data['lucro_prejuizo']:,.2f}")
    
    st.write("Estas são projeções iniciais baseadas na sua ideia de negócio. Recomendamos revisar e ajustar conforme necessário.")

    if st.button("Gerar Novas Projeções"):
        generate_initial_financial_projections(st.session_state['user_idea'])
        st.rerun()

def display_financial_charts(investment, monthly_revenue, monthly_expenses, months):
    profit = monthly_revenue - monthly_expenses
    if profit <= 0:
        st.error("O lucro mensal é negativo ou zero. Ajuste a receita ou despesas.")
        return
    breakeven = investment / profit
    cumulative_profit = [(profit * m) - investment for m in range(1, months + 1)]
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=list(range(1, months + 1)), y=cumulative_profit, mode='lines+markers', name='Lucro Cumulativo'))
    fig.add_hline(y=0, line_dash="dash", line_color="red", annotation_text="Ponto de Equilíbrio")
    fig.update_layout(title='Projeção de Lucro ao Longo do Tempo', xaxis_title='Meses', yaxis_title='Lucro Cumulativo (R$)')
    st.plotly_chart(fig)
    
    st.metric("Ponto de Equilíbrio", f"{breakeven:.1f} meses")
    st.metric("Lucro Mensal Estimado", f"R$ {profit:.2f}")

    # Gráfico de pizza das despesas e receitas
    st.header("Distribuição Financeira")
    labels = ['Despesas Mensais', 'Lucro Mensal']
    values = [monthly_expenses, profit]
    fig_pie = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.3)])
    fig_pie.update_layout(title_text="Despesas vs Lucro")
    st.plotly_chart(fig_pie)