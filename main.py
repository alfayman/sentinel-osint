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

# --- 1. إعداد الصفحة والديزاين "الشرير" (Sentinel Full UI) ---
st.set_page_config(page_title="SENTINEL OSINT TERMINAL", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700&display=swap');
    .stApp { background-color: #050505; background-image: radial-gradient(circle at 50% 50%, #001a2e 0%, #050505 100%); color: #00d4ff; font-family: 'JetBrains Mono', monospace; }
    
    /* Animation ديال العين الأسطورية */
    .cyber-eye-container { display: flex; justify-content: center; margin: 20px 0; perspective: 1000px; }
    .cyber-eye { width: 120px; height: 120px; background: radial-gradient(circle, #00d4ff 10%, #001a2e 50%, #050505 100%); border-radius: 50% 0 50% 0; transform: rotate(45deg); border: 2px solid #00d4ff; box-shadow: 0 0 30px #00d4ff; position: relative; overflow: hidden; animation: eyePulse 4s infinite ease-in-out; }
    .cyber-eye::before { content: ''; position: absolute; top: 20%; left: 20%; width: 60%; height: 60%; background: radial-gradient(circle, #00d4ff 20%, transparent 70%); border-radius: 50%; animation: scanLine 2s infinite linear; }
    .cyber-eye::after { content: ''; position: absolute; width: 100%; height: 2px; background: #00d4ff; top: 50%; box-shadow: 0 0 10px #00d4ff; animation: shutter 3s infinite alternate ease-in-out; }
    
    @keyframes eyePulse { 0%, 100% { transform: rotate(45deg) scale(1); } 50% { transform: rotate(45deg) scale(1.1); } }
    @keyframes scanLine { 0% { transform: translateY(-60px); opacity: 0; } 50% { opacity: 1; } 100% { transform: translateY(60px); opacity: 0; } }
    @keyframes shutter { 0% { height: 2px; top: 50%; } 100% { height: 60px; top: 20%; opacity: 0.2; } }

    .report-box { border: 1px solid #00d4ff; padding: 20px; background: rgba(0, 212, 255, 0.05); border-radius: 10px; }
    .ads-box { background: rgba(255, 255, 255, 0.02); border: 1px dashed #333; text-align: center; padding: 10px; border-radius: 5px; color: #444; margin: 10px 0; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. قاموس اللغات العالمي (All Languages) ---
LANG_MAP = {
    "English": {"title": "SENTINEL OSINT TERMINAL", "up": "Target Acquisition", "scan": "RUN NEURAL SCAN", "rtl": False},
    "Moroccan Darija": {"title": "سنتينل أوسينت تيرمينال", "up": "حط الهدف هنا", "scan": "بدء المسح العصبي", "rtl": True},
    "Spanish": {"title": "TERMINAL SENTINEL", "up": "Adquisición de Objetivo", "scan": "EJECUTAR ESCANEO", "rtl": False},
    "French": {"title": "TERMINAL SENTINEL", "up": "Acquisition de la Cible", "scan": "LANCER LE SCAN", "rtl": False},
    "German": {"title": "SENTINEL TERMINAL", "up": "Zielerfassung", "scan": "SCAN STARTEN", "rtl": False},
    "Russian": {"title": "ТЕРМИНАЛ СЕНТИНЕЛЬ", "up": "Захват цели", "scan": "ЗАПУСТИТЬ СКАНИРОВАНИЕ", "rtl": False},
    "Chinese": {"title": "哨兵 OSINT 終端", "up": "目標獲取", "scan": "執行掃描", "rtl": False},
    "Arabic": {"title": "محطة سنتينل الاستخباراتية", "up": "تحديد الهدف", "scan": "بدء المسح الضوئي", "rtl": True}
}

# --- 3. إعداد الـ AI ---
API_KEY = os.environ.get("AI_INTEGRATIONS_GEMINI_API_KEY")
if API_KEY:
    genai.configure(api_key=API_KEY)
    model = genai.GenerativeModel('gemini-1.5-flash')
else:
    st.error("⚠️ Missing API Key!")

# --- 4. واجهة المستخدم (Sidebar & Tools) ---
st.sidebar.markdown("### 🛠️ SYSTEM TOOLS")
tool1 = st.sidebar.checkbox("✅ AI Deep Scan", value=True)
tool2 = st.sidebar.checkbox("✅ EXIF Extraction", value=True)
tool3 = st.sidebar.checkbox("✅ Geo-Triangulation", value=True)

st.sidebar.divider()
selected_lang = st.sidebar.selectbox("🌐 LANGUAGE / لغة", list(LANG_MAP.keys()))
i18n = LANG_MAP[selected_lang]

st.sidebar.button("💎 UPGRADE TO PRO")
st.sidebar.button("💰 Support (Crypto)")

# --- 5. الصفحة الرئيسية ---
st.markdown("<div class='ads-box'>Google AdSense - Header Banner</div>", unsafe_allow_html=True)

# العين اللي كتحرك وتغمض
st.markdown('<div class="cyber-eye-container"><div class="cyber-eye"></div></div>', unsafe_allow_html=True)
st.markdown(f'<h1 style="text-align: center; color: #00ff41 !important;">{i18n["title"]}</h1>', unsafe_allow_html=True)

# التبويبات (Tabs) كيفما في Replit
tab1, tab2, tab3 = st.tabs(["📡 SIGNAL SCAN", "🔍 EXIF METADATA", "🌍 GEO-ORBIT"])

with tab1:
    col_a, col_b = st.columns([2, 1])
    with col_a:
        uploaded_file = st.file_uploader(i18n["up"], type=["jpg", "png", "jpeg"])
        if uploaded_file:
            st.image(uploaded_file, width=500)
            if st.button(i18n["scan"]):
                with st.spinner("Decrypting pixels..."):
                    try:
                        img = Image.open(uploaded_file)
                        response = model.generate_content([img, f"Analyze this as an OSINT expert. Language: {selected_lang}"])
                        
                        report = response.text
                        if i18n["rtl"]:
                            reshaped = arabic_reshaper.reshape(report)
                            report = get_display(reshaped)
                        
                        st.markdown(f'<div class="report-box">{report}</div>', unsafe_allow_html=True)
                    except Exception as e:
                        st.error(f"Error: {e}")
    with col_b:
        st.markdown("### 🧠 AI NEURAL ANALYSIS")
        st.info("Waiting for target input...")
        st.markdown("<div class='ads-box' style='height: 300px;'>AdSense - Vertical</div>", unsafe_allow_html=True)

with tab2:
    st.markdown("### 🔍 Metadata Extraction")
    st.write("Upload an image in Signal Scan to see EXIF data.")

with tab3:
    st.markdown("### 🌍 Geospatial Orbit")
    st.warning("Deep Triangulation requires Pro License.")

st.markdown("<div class='ads-box'>Google AdSense - Footer Banner</div>", unsafe_allow_html=True)
st.caption("© 2026 Sentinel OSINT v2.5. Ready for AdSense.")
