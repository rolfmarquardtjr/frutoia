import os
from openai import OpenAI
import json

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_questions_with_openai(idea):
    prompt = f"""
Você é um consultor de negócios experiente. Faça 5 perguntas para entender completamente a seguinte ideia de negócio e oferecer a melhor consultoria possível. Inicie diretamente com as perguntas, forneça a resposta em um formato de lista de perguntas somente e mais nada, e não enumere as questões.

Ideia: {idea}

Forneça apenas as perguntas, uma por linha.
"""
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Você é um consultor de negócios experiente."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7
        )
        
        if response.choices and response.choices[0].message:
            questions = response.choices[0].message.content.strip().split('\n')
            # Filtrar linhas vazias e limitar a 5 perguntas
            questions = [q.strip() for q in questions if q.strip()][:5]
            return questions
        else:
            print("A resposta da API não contém perguntas.")
            return []
    except Exception as e:
        print(f'Erro ao gerar perguntas com a API OpenAI: {e}')
        return []

def generate_dashboard_content(idea, questions, answers):
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
            "tarefas": ["", "", "", ""]
        }},
        {{
            "titulo": "",
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
        response = client.chat.completions.create(
            model='gpt-4o-mini',
            messages=[
                {"role": "system", "content": "Você é um consultor de negócios experiente."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.5
        )
        content = response.choices[0].message.content.strip()
        json_start = content.find('{')
        json_end = content.rfind('}') + 1
        json_str = content[json_start:json_end]
        dashboard_data = json.loads(json_str)
        return dashboard_data
    except Exception as e:
        print(f'Erro ao gerar painel de controle: {e}')
        return None

def generate_networking_suggestions(idea):
    prompt = f"""
Com base na seguinte ideia de negócio, forneça 5 sugestões de eventos, comunidades ou recursos online onde o empreendedor possa se conectar com outras pessoas na mesma área.

Ideia: {idea}

Forneça apenas as sugestões em formato de lista.
"""
    try:
        response = client.chat.completions.create(
            model='gpt-4o-mini',
            messages=[
                {"role": "system", "content": "Você é um consultor de negócios experiente."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.5
        )
        content = response.choices[0].message.content.strip()
        suggestions = [s.strip('- ') for s in content.strip().split('\n') if s.strip()]
        return suggestions
    except Exception as e:
        print(f'Erro ao obter sugestões: {e}')
        return []

def generate_legal_plan(idea):
    prompt = f"""
Você é um consultor jurídico especializado em direito empresarial. Forneça um plano de ação geral para ajudar o empreendedor a iniciar legalmente o seguinte negócio:

Ideia: {idea}

O plano deve incluir os principais passos legais necessários, como registro de empresa, obtenção de licenças, requisitos fiscais, entre outros. Forneça a resposta em formato de lista, sem introdução ou conclusão.
"""
    try:
        response = client.chat.completions.create(
            model='gpt-4o-mini',
            messages=[
                {"role": "system", "content": "Você é um consultor jurídico especializado em direito empresarial."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.5
        )
        content = response.choices[0].message.content.strip()
        legal_steps = [step.strip('- ') for step in content.strip().split('\n') if step.strip()]
        return '\n'.join([f"- {step}" for step in legal_steps])
    except Exception as e:
        print(f'Erro ao gerar plano jurídico: {e}')
        return ''

def get_assistant_response(messages):
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages,
            temperature=0.7
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"Erro ao obter resposta do assistente: {e}")
        return None