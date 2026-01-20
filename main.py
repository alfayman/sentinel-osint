import streamlit as st
import os
import google.generativeai as genai
import arabic_reshaper
from bidi.algorithm import import get_display
from fpdf import FPDF
import pandas as pd
from PIL import Image

# --- إعداد الصفحة ---
st.set_page_config(page_title="Sentinel OSINT", layout="wide")

# --- جلب مفتاح API من Secrets ---
API_KEY = os.environ.get("AI_INTEGRATIONS_GEMINI_API_KEY")

if API_KEY:
    genai.configure(api_key=API_KEY)
    model = genai.GenerativeModel('gemini-pro')
else:
    st.error("Missing Gemini API Key. Please add it to Streamlit Secrets.")

# --- واجهة المستخدم ---
st.title("SENTINEL OSINT")
st.subheader("FORENSIC IMAGE INTELLIGENCE & ANALYSIS")

uploaded_file = st.file_uploader("Drop image for forensic analysis", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_column_width=True)
    
    if st.button("Analyze Image"):
        try:
            # هنا كينوض الـ Agent يخدم
            response = model.generate_content(["Analyze this image for forensic details:", image])
            st.write("### Analysis Results:")
            st.write(response.text)
        except Exception as e:
            st.error(f"Analysis failed: {e}")

# --- وظيفة إنشاء تقرير PDF ---
def create_pdf_report(metadata_text, report_text):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="Sentinel OSINT - Forensic Report", ln=True, align='C')
    pdf.multi_cell(0, 10, txt=report_text)
    return pdf.output(dest='S').encode('latin-1')

st.sidebar.markdown("### Settings")
st.sidebar.info("System Status: Operational")
