import streamlit as st
from fpdf import FPDF
import base64
import json

def export_to_pdf():
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    
    pdf.cell(200, 10, txt="Plano de Negócios", ln=True, align='C')
    pdf.cell(200, 10, txt=f"Ideia: {st.session_state.get('user_idea', '')}", ln=True)
    
    pdf.cell(200, 10, txt="Resumo do Dashboard", ln=True)
    if 'dashboard_data' in st.session_state:
        dashboard = st.session_state['dashboard_data']
        pdf.multi_cell(0, 10, txt=json.dumps(dashboard, indent=4, ensure_ascii=False))
    
    # Adicionar mais seções conforme necessário
    if 'swot' in st.session_state:
        pdf.add_page()
        pdf.cell(200, 10, txt="Análise SWOT", ln=True, align='C')
        for category, items in st.session_state['swot'].items():
            pdf.cell(200, 10, txt=f"{category.capitalize()}:", ln=True)
            for item in items:
                pdf.cell(200, 10, txt=f"- {item}", ln=True)
    
    if 'expenses' in st.session_state:
        pdf.add_page()
        pdf.cell(200, 10, txt="Controle de Gastos", ln=True, align='C')
        for expense in st.session_state['expenses']:
            pdf.cell(200, 10, txt=f"{expense['name']}: R$ {expense['amount']:.2f}", ln=True)
    
    pdf_output = pdf.output(dest='S').encode('latin-1')
    b64 = base64.b64encode(pdf_output).decode()
    href = f'<a href="data:application/pdf;base64,{b64}" download="plano_de_negocios.pdf">Baixar PDF</a>'
    st.markdown(href, unsafe_allow_html=True)