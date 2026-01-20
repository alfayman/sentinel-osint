import streamlit as st
import os
import time
import datetime
from PIL import Image
from PIL.ExifTags import TAGS
import google.generativeai as genai
import arabic_reshaper
from bidi.algorithm import get_display
from fpdf import FPDF

# --- 1. إعدادات الثيم (Sentinel Cyber-UI) ---
st.set_page_config(page_title="SENTINEL OSINT PRO", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700&display=swap');
    .stApp { background-color: #050505; background-image: radial-gradient(circle at 50% 50%, #001a2e 0%, #050505 100%); color: #00d4ff; font-family: 'JetBrains Mono', monospace; }
    
    /* أنيمايشن العين الأسطورية - رماش أفقي وبدون ليزر */
    .eye-box { display: flex; justify-content: center; margin: 30px 0; perspective: 1000px; }
    .cyber-eye {
        width: 140px; height: 140px; 
        background: radial-gradient(circle, #00d4ff 0%, #003a4d 40%, #050505 80%);
        border-radius: 60% 0 60% 0; transform: rotate(45deg);
        border: 3px solid #00d4ff; box-shadow: 0 0 50px rgba(0, 212, 255, 0.4);
        position: relative; overflow: hidden;
        animation: eyePulse 4s infinite ease-in-out;
    }
    /* جفون العين الأفقية */
    .cyber-eye::before, .cyber-eye::after {
        content: ''; position: absolute; width: 0%; height: 100%;
        background: #050505; top: 0; z-index: 2;
        animation: horizontalBlink 5s infinite ease-in-out;
    }
    .cyber-eye::before { left: 0; border-right: 1px solid #00d4ff; }
    .cyber-eye::after { right: 0; border-left: 1px solid #00d4ff; }

    @keyframes eyePulse { 0%, 100% { transform: rotate(45deg) scale(1); filter: brightness(1); } 50% { transform: rotate(45deg) scale(1.05); filter: brightness(1.2); } }
    @keyframes horizontalBlink { 0%, 90%, 100% { width: 0%; } 95% { width: 55%; } }

    .report-box { border: 1px solid #00d4ff; padding: 25px; background: rgba(0, 212, 255, 0.05); backdrop-filter: blur(15px); border-radius: 15px; box-shadow: inset 0 0 20px rgba(0, 212, 255, 0.1); }
    .ad-slot { background: rgba(255, 255, 255, 0.02); border: 1px dashed rgba(0, 212, 255, 0.2); text-align: center; padding: 15px; margin: 15px 0; color: #444; border-radius: 8px; }
    .trace-log { font-size: 11px; color: #00ff41; font-family: 'Courier New', monospace; margin: 2px 0; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. قاموس اللغات العالمي (10+ لغات) ---
LANG_MAP = {
    "English": {"title": "SENTINEL OSINT TERMINAL", "up": "Drop Target Image", "scan": "EXECUTE NEURAL SCAN", "rtl": False},
    "Moroccan Darija": {"title": "سنتينل أوسينت تيرمينال", "up": "حط التصويرة هنا", "scan": "بدء المسح العصبي", "rtl": True},
    "Spanish": {"title": "TERMINAL SENTINEL OSINT", "up": "Subir Imagen Objetivo", "scan": "EJECUTAR ANÁLISIS", "rtl": False},
    "French": {"title": "TERMINAL SENTINEL", "up": "Charger la cible", "scan": "LANCER L'ANALYSE", "rtl": False},
    "Arabic": {"title": "محطة سنتينل للاستخبارات", "up": "تحديد الهدف البصري", "scan": "تحليل استخباراتي", "rtl": True},
    "German": {"title": "SENTINEL TERMINAL", "up": "Bild hochladen", "scan": "ANALYSE STARTEN", "rtl": False},
    "Russian": {"title": "ТЕРМИНАЛ СЕНТИНЕЛЬ", "up": "Загрузить цель", "scan": "НАЧАТЬ СКАН", "rtl": False},
    "Japanese": {"title": "センチネル OSINT ターミナル", "up": "ターゲット画像", "scan": "スキャン実行", "rtl": False},
    "Turkish": {"title": "SENTINEL OSINT TERMİNALİ", "up": "Hedef Resmi Yükle", "scan": "ANALİZ ET", "rtl": False},
    "Portuguese": {"title": "TERMINAL SENTINEL", "up": "Carregar Imagem", "scan": "EXECUTAR ANÁLISE", "rtl": False}
}

# --- 3. إعداد الـ AI (Gemini 1.5 Flash) ---
API_KEY = os.environ.get("AI_INTEGRATIONS_GEMINI_API_KEY")
if API_KEY:
    genai.configure(api_key=API_KEY)
    model = genai.GenerativeModel('gemini-1.5-flash')
else:
    st.error("⚠️ AI Key Missing! System Offline.")

# --- 4. Sidebar (The 3 Professional Tools + Trace) ---
with st.sidebar:
    st.markdown("### 🛠️ SYSTEM TOOLS")
    st.checkbox("✅ AI Deep Scan (Active)", value=True)
    st.checkbox("✅ EXIF Extraction (Active)", value=True)
    st.checkbox("✅ Geo-Triangulation (Active)", value=True)
    st.divider()
    selected_lang = st.selectbox("🌐 LANGUAGE SELECTION", list(LANG_MAP.keys()))
    i18n = LANG_MAP[selected_lang]
    st.divider()
    st.button("💎 UPGRADE TO PRO (UNLIMITED)")
    st.button("💰 SUPPORT (BITCOIN/ETH)")
    st.divider()
    st.markdown("### 📡 LIVE TRACE LOGS")
    st.markdown('<p class="trace-log">> Initializing Uplink...</p>', unsafe_allow_html=True)
    st.markdown('<p class="trace-log">> Bypassing Firewalls...</p>', unsafe_allow_html=True)
    st.markdown('<p class="trace-log">> Node: Classified-Alpha</p>', unsafe_allow_html=True)

# --- 5. الواجهة الرئيسية ---
st.markdown("<div class='ad-slot'>GOOGLE ADSENSE - TOP LEADERBOARD</div>", unsafe_allow_html=True)

# العين اللي كترمق أفقيًا
st.markdown('<div class="eye-box"><div class="cyber-eye"></div></div>', unsafe_allow_html=True)
st.markdown(f'<h1 style="text-align: center; color: #00ff41 !important;">{i18n["title"]}</h1>', unsafe_allow_html=True)

# نظام التبويبات (Tabs)
tab1, tab2, tab3 = st.tabs(["📡 SIGNAL SCAN", "🔍 EXIF DATA", "🌍 GEO-ORBIT"])

with tab1:
    col_l, col_r = st.columns([2, 1])
    with col_l:
        uploaded_file = st.file_uploader(i18n["up"], type=["jpg", "png", "jpeg"])
        if uploaded_file:
            st.image(uploaded_file, caption="TARGET IDENTIFIED", use_column_width=True)
            if st.button(i18n["scan"]):
                with st.spinner("Agent Sentinel decoding signal..."):
                    try:
                        img = Image.open(uploaded_file)
                        response = model.generate_content([img, f"Provide a deep OSINT report in {selected_lang}."])
                        report = response.text
                        if i18n["rtl"]:
                            report = get_display(arabic_reshaper.reshape(report))
                        
                        st.markdown(f'<div class="report-box">{report}</div>', unsafe_allow_html=True)
                        
                        # PDF Export
                        pdf = FPDF()
                        pdf.add_page()
                        pdf.set_font("Arial", size=12)
                        pdf.multi_cell(0, 10, txt=response.text.encode('latin-1', 'ignore').decode('latin-1'))
                        st.download_button("📥 DOWNLOAD REPORT", pdf.output(dest='S').encode('latin-1'), "sentinel.pdf")
                    except Exception as e:
                        st.error(f"SCAN FAILURE: {e}")
    with col_r:
        st.markdown("### 🧠 SYSTEM ANALYSIS")
        st.info("Status: Waiting for Input")
        st.markdown("<div class='ad-slot' style='height:400px;'>ADSENSE - VERTICAL BANNER</div>", unsafe_allow_html=True)

with tab2:
    st.markdown("### 🔍 METADATA EXTRACTION")
    st.warning("Upload image in Signal Scan to decrypt headers.")

with tab3:
    st.markdown("### 🌍 GLOBAL TRIANGULATION")
    st.info("Searching for visual landmarks in orbital database...")

st.markdown("<div class='ad-slot'>GOOGLE ADSENSE - FOOTER BANNER</div>", unsafe_allow_html=True)
st.caption("© 2026 Sentinel OSINT v2.5 | Security Clearance: Classified")
