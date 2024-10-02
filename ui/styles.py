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
            text-align: center; /* Centralizando os títulos */
        }
        /* Botões */
        .stButton>button {
            background-color: #2980b9;
            color: white;
            border-radius: 5px;
            padding: 10px 24px;
            border: none;
            transition: background-color 0.3s ease, transform 0.3s ease;
        }
        .stButton>button:hover {
            background-color: #1f6391;
            transform: scale(1.05); /* Efeito de zoom ao passar o mouse */
        }
        /* Sidebar */
        .css-1d391kg {
            background-color: #2c3e50 !important; /* Cor de fundo do sidebar */
        }
        .css-1d391kg .element-container {
            background-color: #2c3e50 !important; /* Cor de fundo dos elementos do sidebar */
        }
        .css-1d391kg h1, .css-1d391kg h2, .css-1d391kg h3, .css-1d391kg h4, .css-1d391kg h5, .css-1d391kg h6, .css-1d391kg p {
            color: #ffffff !important; /* Cor da fonte dos títulos e parágrafos no sidebar */
        }
        .css-1d391kg .stButton>button {
            background-color: #1f6391 !important; /* Cor de fundo dos botões no sidebar */
            color: white !important;
        }
        .css-1d391kg .stButton>button:hover {
            background-color: #145a86 !important; /* Cor de fundo dos botões no sidebar ao passar o mouse */
        }
        .css-1d391kg .stExpander {
            background-color: #2c3e50 !important; /* Cor de fundo dos expansores no sidebar */
            color: #ffffff !important; /* Cor da fonte dos expansores no sidebar */
        }
        .css-1d391kg .stExpander summary {
            color: #ffffff !important; /* Cor da fonte do sumário dos expansores no sidebar */
        }
        .css-1d391kg .stExpander div {
            color: #ffffff !important; /* Cor da fonte do conteúdo dos expansores no sidebar */
        }
        .css-1d391kg .stMarkdown hr {
            border-top: 1px solid #ffffff !important; /* Cor da linha horizontal no sidebar */
        }

        /* Atualização do estilo do menu para torná-lo mais atraente */
        .stRadio > div {
            background-color: #2c3e50 !important;          /* Cor de fundo azul escuro */
            border-radius: 8px;                 /* Bordas arredondadas */
            padding: 10px 20px;                 /* Espaçamento interno */
            font-size: 16px;                    /* Tamanho da fonte */
            color: #ffffff !important;                     /* Cor da fonte branca */
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);  /* Sombra sutil */
            transition: background-color 0.3s ease;    /* Transição suave */
        }
        .stRadio > div:hover {
            background-color: #1f6391 !important;          /* Cor de fundo ao passar o mouse */
        }
        .stRadio > div > label {
            color: #ffffff !important;                     /* Cor da fonte branca */
        }
        .stRadio > div > div[role="radiogroup"] > label {
            color: #ffffff !important;                     /* Cor da fonte branca */
        }
        .stRadio > div > div[role="radiogroup"] > label:hover {
            background-color: #1f6391 !important;          /* Cor de fundo ao passar o mouse */
        }

        /* Estilização dos ícones do menu */
        .stRadio > div > div[role="radiogroup"] > label > div {
            display: flex;
            align-items: center;
        }
        .stRadio > div > div[role="radiogroup"] > label > div > svg {
            margin-right: 10px;
        }

        /* Barra de progresso */
        .stProgress > div > div {
            background-color: #2980b9 !important; /* Cor da barra de progresso */
        }

        /* Centralizando o conteúdo */
        .center-content {
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            text-align: center;
        }

        /* Estilização da análise SWOT */
        .swot-container {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 20px;
            margin-top: 20px;
        }
        .swot-item {
            background-color: #ffffff;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            text-align: center;
            position: relative;
        }
        .swot-item h3 {
            margin-bottom: 10px;
        }
        .swot-item ul {
            list-style-type: none;
            padding: 0;
        }
        .swot-item ul li {
            margin-bottom: 5px;
            text-align: left;
        }
        .swot-item.forcas {
            border-left: 5px solid #2ecc71;
        }
        .swot-item.fraquezas {
            border-left: 5px solid #e74c3c;
        }
        .swot-item.oportunidades {
            border-left: 5px solid #3498db;
        }
        .swot-item.ameacas {
            border-left: 5px solid #e67e22;
        }
        .swot-icon {
            position: absolute;
            top: -20px;
            left: 50%;
            transform: translateX(-50%);
            background-color: #ffffff;
            border-radius: 50%;
            padding: 10px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }
        .swot-icon img {
            width: 30px;
            height: 30px;
        }
    </style>
    """, unsafe_allow_html=True)