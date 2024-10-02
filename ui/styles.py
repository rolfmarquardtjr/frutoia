import streamlit as st

def load_css():
    st.markdown("""
    <style>
        /* Estilização geral */
        .stApp {
            background-color: #f0f2f6;
            font-family: 'Arial', sans-serif;
        }
        /* Títulos */
        h1, h2, h3, h4, h5, h6 {
            color: #2c3e50;
        }
        /* Botões */
        .stButton>button {
            background-color: #2980b9;
            color: white;
            border-radius: 5px;
            padding: 10px 24px;
            border: none;
            transition: background-color 0.3s ease;
        }
        .stButton>button:hover {
            background-color: #1f6391;
        }
        /* Sidebar */
        .css-1d391kg {
            background-color: #ffffff;
            border-right: 1px solid #e0e0e0;
        }
        /* Expansores */
        .stExpander {
            background-color: #ffffff;
            border-radius: 5px;
            border: 1px solid #e0e0e0;
        }
        /* Métricas */
        .metric-container {
            background-color: #ecf0f1;
            padding: 15px;
            border-radius: 10px;
            text-align: center;
            margin-bottom: 10px;
        }
        .metric-title {
            font-size: 18px;
            color: #7f8c8d;
        }
        .metric-value {
            font-size: 24px;
            font-weight: bold;
            color: #2c3e50;
        }
        /* Cards */
        .card {
            background-color: #ffffff;
            padding: 20px;
            border-radius: 10px;
            margin-bottom: 20px;
            border: 1px solid #e0e0e0;
        }
        /* Kanban Board */
        .kanban-board {
            display: flex;
            justify-content: space-between;
        }
        .kanban-column {
            background-color: #ecf0f1;
            padding: 10px;
            border-radius: 10px;
            width: 30%;
        }
        .kanban-item {
            background-color: #ffffff;
            padding: 10px;
            border-radius: 5px;
            margin-bottom: 10px;
            cursor: pointer;
            border: 1px solid #bdc3c7;
        }
        /* Progress Bar */
        .progress-bar {
            width: 100%;
            background-color: #ecf0f1;
            border-radius: 5px;
            margin-bottom: 20px;
        }
        .progress {
            height: 20px;
            background-color: #2980b9;
            border-radius: 5px;
            text-align: center;
            color: white;
        }
        /* Achievements */
        .achievement {
            background-color: #ffffff;
            padding: 15px;
            border-radius: 10px;
            margin-bottom: 10px;
            border: 1px solid #e0e0e0;
            display: flex;
            align-items: center;
        }
        .achievement-icon {
            font-size: 30px;
            margin-right: 15px;
            color: #f1c40f;
        }
        .achievement-text {
            font-size: 16px;
            color: #2c3e50;
        }
    </style>
    """, unsafe_allow_html=True)