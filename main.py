import streamlit as st
import os
import time
import datetime
from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS
import google.generativeai as genai
import arabic_reshaper
from bidi.algorithm import get_display
from fpdf import FPDF

# --- 1. إعدادات الثيم الاحترافي (Replit Style) ---
st.set_page_config(page_title="SENTINEL OSINT PRO", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700&display=swap');
    .stApp { background-color: #050505; background-image: radial-gradient(circle at 50% 50%, #001a2e 0%, #050505 100%); color: #00d4ff; font-family: 'JetBrains Mono', monospace; }
    h1, h2, h3, p, span, label { color: #00d4ff !important; text-shadow: 0 0 10px rgba(0, 212, 255, 0.5); }
    .stButton > button { background: linear-gradient(45deg, #00d4ff, #005f73); color: white; border: none; font-weight: bold; width: 100%; box-shadow: 0 4px 15px rgba(0, 212, 255, 0.3); }
    .report-box { border: 1px solid #00d4ff; padding: 25px; background: rgba(0, 212, 255, 0.05); backdrop-filter: blur(10px); border-radius: 10px; }
    .ad-slot { background: rgba(255, 255, 255, 0.03); border: 1px dashed rgba(0, 212, 255, 0.1); color: #444; text-align: center; padding: 15px; margin: 15px 0; border-radius: 8px; }
    .cyber-eye { width: 100px; height: 100px; background: radial-gradient(circle, #00d4ff 10%, #001a2e 100%); border-radius: 50% 0 50% 0; transform: rotate(45deg); border: 2px solid #00d4ff; margin: auto; animation: eyePulse 4s infinite; }
    @keyframes eyePulse { 0%, 100% { transform: rotate(45deg) scale(1); } 50% { transform: rotate(45deg) scale(1.1); } }
    </style>
    """, unsafe_allow_html=True)

# --- 2. قاموس اللغات العالمي ---
LANG_MAP = {
    "English": {"title": "SENTINEL OSINT", "scan": "ANALYZE IMAGE", "rep": "Forensic Report", "up": "Drop Image", "rtl": False},
    "Moroccan Darija": {"title": "سنتينل أوسينت", "scan": "حلل التصويرة", "rep": "تقرير جنائي", "up": "حط التصويرة", "rtl": True},
    "Arabic": {"title": "سنتينل للتحليل", "scan": "بدء التحليل", "rep": "تقرير استخباراتي", "up": "رفع الصورة", "rtl": True},
    "French": {"title": "SENTINEL PRO", "scan": "ANALYSER", "rep": "Rapport", "up": "Charger", "rtl": False}
}

# --- 3. إعداد الـ AI والوظائف ---
API_KEY = os.environ.get("AI_INTEGRATIONS_GEMINI_API_KEY")
if API_KEY:
    genai.configure(api_key=API_KEY)
    model = genai.GenerativeModel('gemini-1.5-flash')
else:
    st.error("⚠️ AI Key Missing!")

def get_exif(uploaded_file):
    try:
        img = Image.open(uploaded_file)
        exif = img._getexif()
        return {TAGS.get(tag, tag): value for tag, value in exif.items()} if exif else None
    except: return None

# --- 4. الواجهة الرئيسية ---
st.sidebar.title("Settings")
selected_lang = st.sidebar.selectbox("Language / لغة", list(LANG_MAP.keys()))
i18n = LANG_MAP[selected_lang]

st.markdown("<div class='ad-slot'>ADSENSE HEADER AD</div>", unsafe_allow_html=True)

# اللوغو المتحرك (Cyber Eye)
st.markdown('<div class="cyber-eye"></div>', unsafe_allow_html=True)
st.markdown(f'<h1 style="text-align: center;">{i18n["title"]}</h1>', unsafe_allow_html=True)

col1, col2 = st.columns([3, 1])

with col1:
    uploaded_file = st.file_uploader(i18n["up"], type=["jpg", "jpeg", "png"])
    if uploaded_file:
        img = Image.open(uploaded_file)
        st.image(img, caption="Evidence Source", width=500)
        
        if st.button(i18n["scan"]):
            with st.spinner("Neural Uplink Established..."):
                try:
                    # سحب EXIF
                    exif_data = get_exif(uploaded_file)
                    # تحليل AI
                    prompt = f"Perform a professional OSINT forensic analysis. Language: {selected_lang}. Metadata: {str(exif_data)}"
                    response = model.generate_content([img, prompt])
                    
                    st.markdown(f"### 🕵️ {i18n['rep']}")
                    report_content = response.text
                    
                    # دعم العربية/الدارجة (RTL)
                    if i18n["rtl"]:
                        reshaped = arabic_reshaper.reshape(report_content)
                        report_content = get_display(reshaped)
                    
                    st.markdown(f'<div class="report-box">{report_content}</div>', unsafe_allow_html=True)
                    
                    # PDF Download
                    pdf = FPDF()
                    pdf.add_page()
                    pdf.set_font("Arial", size=12)
                    pdf.multi_cell(0, 10, txt=response.text.encode('latin-1', 'ignore').decode('latin-1'))
                    st.download_button("📥 DOWNLOAD REPORT", pdf.output(dest='S').encode('latin-1'), "report.pdf")
                except Exception as e:
                    st.error(f"Error: {e}")

with col2:
    st.sidebar.success("System: Operational 🟢")
    st.sidebar.markdown(f"**Uplink**: Secure\n**Credits**: 10/10")
    st.sidebar.markdown("---")
    st.sidebar.markdown("<div class='ad-slot' style='height: 400px;'>ADSENSE SIDEBAR</div>", unsafe_allow_html=True)

st.markdown("<div class='ad-slot'>ADSENSE FOOTER AD</div>", unsafe_allow_html=True)
