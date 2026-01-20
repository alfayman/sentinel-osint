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

# --- 1. ثيم Replit الاحترافي (Sentinel Dark Theme) ---
st.set_page_config(page_title="SENTINEL OSINT PRO", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700&display=swap');
    .stApp { background-color: #050505; background-image: radial-gradient(circle at 50% 50%, #001a2e 0%, #050505 100%); color: #00d4ff; font-family: 'JetBrains Mono', monospace; }
    h1, h2, h3, p, span, label { color: #00d4ff !important; text-shadow: 0 0 10px rgba(0, 212, 255, 0.5); }
    .stButton > button { background: linear-gradient(45deg, #00d4ff, #005f73); color: white; border: none; font-weight: bold; width: 100%; box-shadow: 0 4px 15px rgba(0, 212, 255, 0.3); }
    .report-box { border: 1px solid #00d4ff; padding: 25px; background: rgba(0, 212, 255, 0.05); backdrop-filter: blur(10px); border-radius: 10px; }
    .adsense-placeholder { background: rgba(255, 255, 255, 0.03); border: 1px dashed rgba(0, 212, 255, 0.1); color: #444; text-align: center; padding: 15px; margin: 15px 0; border-radius: 8px; }
    
    /* Cyber Eye Animation (The Replit Soul) */
    .cyber-eye-container { display: flex; justify-content: center; margin: 20px 0; }
    .cyber-eye { width: 100px; height: 100px; background: radial-gradient(circle, #00d4ff 10%, #001a2e 100%); border-radius: 50% 0 50% 0; transform: rotate(45deg); border: 2px solid #00d4ff; animation: eyePulse 4s infinite; }
    @keyframes eyePulse { 0%, 100% { transform: rotate(45deg) scale(1); box-shadow: 0 0 30px #00d4ff; } 50% { transform: rotate(45deg) scale(1.1); box-shadow: 0 0 50px #00d4ff; } }
    </style>
    """, unsafe_allow_html=True)

# --- 2. نظام اللغات (بما فيها الإسبانية) ---
LANG_MAP = {
    "English": {"title": "SENTINEL OSINT", "scan": "ANALYZE IMAGE", "rep": "Forensic Report", "up": "Drop Image", "credits": "Credits", "rtl": False},
    "Spanish": {"title": "SENTINEL OSINT", "scan": "EJECUTAR ANÁLISIS", "rep": "Informe Forense", "up": "Subir Imagen", "credits": "Créditos", "rtl": False},
    "Moroccan Darija": {"title": "سنتينل أوسينت", "scan": "حلل التصويرة", "rep": "تقرير جنائي", "up": "حط التصويرة", "credits": "الكريدي", "rtl": True},
    "Arabic": {"title": "سنتينل للتحليل", "scan": "بدء التحليل", "rep": "تقرير استخباراتي", "up": "رفع الصورة", "credits": "الرصيد", "rtl": True},
    "French": {"title": "SENTINEL PRO", "scan": "ANALYSER", "rep": "Rapport", "up": "Charger", "credits": "Crédits", "rtl": False}
}

# --- 3. إعداد الـ AI (Gemini 1.5 Flash) ---
API_KEY = os.environ.get("AI_INTEGRATIONS_GEMINI_API_KEY")
if API_KEY:
    genai.configure(api_key=API_KEY)
    model = genai.GenerativeModel('gemini-1.5-flash')
else:
    st.error("⚠️ AI Key Missing!")

# --- 4. نظام الـ Credits والـ Reset ---
if 'credits' not in st.session_state: st.session_state.credits = 3
if 'last_reset' not in st.session_state: st.session_state.last_reset = datetime.date.today()
if st.session_state.last_reset != datetime.date.today():
    st.session_state.credits = 3
    st.session_state.last_reset = datetime.date.today()

# --- 5. الواجهة الرئيسية ---
selected_lang = st.sidebar.selectbox("🌐 Language", list(LANG_MAP.keys()))
i18n = LANG_MAP[selected_lang]

# AdSense Header
st.markdown("<div class='adsense-placeholder'>Google AdSense - Header Banner (728x90)</div>", unsafe_allow_html=True)

# Replit Cyber Eye Logo
st.markdown('<div class="cyber-eye-container"><div class="cyber-eye"></div></div>', unsafe_allow_html=True)
st.markdown(f'<h1 style="text-align: center;">{i18n["title"]}</h1>', unsafe_allow_html=True)
st.markdown(f'<p style="text-align: center; opacity: 0.7;">{i18n["credits"]}: {st.session_state.credits}/3</p>', unsafe_allow_html=True)

col1, col2 = st.columns([3, 1])

with col1:
    uploaded_file = st.file_uploader(i18n["up"], type=["jpg", "jpeg", "png"])
    if uploaded_file:
        st.image(uploaded_file, caption="Target Image", width=500)
        
        if st.button(i18n["scan"]):
            if st.session_state.credits > 0:
                with st.spinner("Decoding pixels..."):
                    try:
                        img = Image.open(uploaded_file)
                        prompt = f"Perform a professional OSINT analysis. Report in {selected_lang}."
                        response = model.generate_content([img, prompt])
                        
                        st.session_state.credits -= 1
                        st.success("SCAN COMPLETE")
                        
                        report_text = response.text
                        if i18n["rtl"]:
                            reshaped = arabic_reshaper.reshape(report_text)
                            report_text = get_display(reshaped)
                        
                        st.markdown(f"### 🕵️ {i18n['rep']}")
                        st.markdown(f'<div class="report-box">{report_text}</div>', unsafe_allow_html=True)
                        
                        # PDF Download
                        pdf = FPDF()
                        pdf.add_page()
                        pdf.set_font("Arial", size=12)
                        pdf.multi_cell(0, 10, txt=response.text.encode('latin-1', 'ignore').decode('latin-1'))
                        st.download_button("📥 DOWNLOAD PDF", pdf.output(dest='S').encode('latin-1'), "report.pdf")
                    except Exception as e:
                        st.error(f"Error: {e}")
            else:
                st.error("CREDIT LIMIT REACHED. Upgrade to Pro.")

with col2:
    st.sidebar.markdown("### 🔐 PRO FEATURES")
    st.sidebar.checkbox("Batch Scan", disabled=True)
    st.sidebar.checkbox("Deep Geo-Location", disabled=True)
    st.sidebar.button("🚀 UPGRADE TO PRO")
    
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 🌍 NETWORK TRACE")
    st.sidebar.code("Uplink: SECURE\nNode: CLASSIFIED\nEncryption: AES-256")
    
    # AdSense Sidebar
    st.markdown("<div class='adsense-placeholder' style='height: 400px;'>AdSense - Vertical Skyscraper</div>", unsafe_allow_html=True)

# Footer
st.markdown("<div class='adsense-placeholder'>Google AdSense - Footer Banner</div>", unsafe_allow_html=True)
st.caption("© 2026 Sentinel OSINT. Ready for Ads & Monetization.")
