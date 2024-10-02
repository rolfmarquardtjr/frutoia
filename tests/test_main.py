import unittest
import sys
import os

# Adiciona o diretório raiz do projeto ao PATH para importar módulos corretamente
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from modules.authentication import create_user, check_user
from modules.dashboard import generate_and_store_dashboard
from modules.swot_analysis import generate_swot_chart
from modules.financial_projections import display_financial_charts
from utils.database import save_session_data, load_session_data
from api.openai_api import generate_dashboard_content, generate_networking_suggestions

class TestMainFunctionalities(unittest.TestCase):

    def setUp(self):
        # Configurações iniciais para os testes
        self.test_user = "testuser"
        self.test_password = "testpassword"

    def test_user_creation_and_authentication(self):
        # Teste de criação de usuário
        self.assertTrue(create_user(self.test_user, self.test_password))
        
        # Teste de autenticação
        self.assertTrue(check_user(self.test_user, self.test_password))
        
        # Teste de autenticação com senha incorreta
        self.assertFalse(check_user(self.test_user, "wrongpassword"))

    def test_dashboard_generation(self):
        # Mock de dados para teste
        idea = "Uma loja de roupas sustentáveis"
        questions = ["Qual é o seu público-alvo?", "Quais são seus principais produtos?"]
        answers = ["Jovens conscientes", "Camisetas e calças de materiais reciclados"]

        # Teste de geração de dashboard
        dashboard_data = generate_dashboard_content(idea, questions, answers)
        self.assertIsNotNone(dashboard_data)
        self.assertIn("visao_geral", dashboard_data)
        self.assertIn("metricas", dashboard_data)
        self.assertIn("etapas", dashboard_data)

    def test_swot_analysis(self):
        # Mock de dados SWOT
        swot_data = {
            'forças': ['Produtos sustentáveis', 'Marca forte'],
            'fraquezas': ['Custos altos', 'Distribuição limitada'],
            'oportunidades': ['Crescimento do mercado eco-friendly', 'Parcerias com influenciadores'],
            'ameaças': ['Concorrência', 'Mudanças na regulamentação']
        }

        # Teste de geração de gráfico SWOT
        swot_chart = generate_swot_chart(swot_data)
        self.assertIsNotNone(swot_chart)

    def test_financial_projections(self):
        # Mock de dados financeiros
        investment = 100000
        monthly_revenue = 20000
        monthly_expenses = 15000
        months = 12

        # Teste de geração de projeções financeiras
        charts = display_financial_charts(investment, monthly_revenue, monthly_expenses, months)
        self.assertIsNotNone(charts)

    def test_session_data_persistence(self):
        # Mock de dados de sessão
        session_data = {
            'user_idea': 'Loja de roupas sustentáveis',
            'swot': {'forças': ['Produtos eco-friendly'], 'fraquezas': ['Custos altos']},
            'expenses': [{'name': 'Aluguel', 'amount': 2000}]
        }

        # Teste de salvamento e carregamento de dados de sessão
        save_session_data(self.test_user, session_data)
        loaded_data = load_session_data(self.test_user)
        self.assertEqual(session_data, loaded_data)

    def test_networking_suggestions(self):
        idea = "Uma loja de roupas sustentáveis"
        suggestions = generate_networking_suggestions(idea)
        self.assertIsInstance(suggestions, list)
        self.assertTrue(len(suggestions) > 0)

if __name__ == '__main__':
    unittest.main()