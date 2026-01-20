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

# --- 1. إعدادات الثيم (Cyber-Sentinel UI) ---
st.set_page_config(page_title="SENTINEL OSINT PRO", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700&display=swap');
    .stApp { background-color: #050505; background-image: radial-gradient(circle at 50% 50%, #001a2e 0%, #050505 100%); color: #00d4ff; font-family: 'JetBrains Mono', monospace; }
    
    /* أنيمايشن العين المطورة */
    .eye-box { display: flex; justify-content: center; margin: 20px 0; }
    .cyber-eye {
        width: 130px; height: 130px; 
        background: radial-gradient(circle, #00d4ff 5%, #005f73 40%, #050505 100%);
        border-radius: 60% 0 60% 0; transform: rotate(45deg);
        border: 3px solid #00d4ff; box-shadow: 0 0 40px #00d4ff;
        position: relative; overflow: hidden;
        animation: eyePulse 3s infinite ease-in-out;
    }
    .cyber-eye::before { /* خط السكان */
        content: ''; position: absolute; width: 200%; height: 2px; 
        background: #00ff41; top: 0; left: -50%;
        box-shadow: 0 0 15px #00ff41; animation: scanning 2s infinite linear;
    }
    .cyber-eye::after { /* جفن العين */
        content: ''; position: absolute; width: 100%; height: 100%;
        background: #050505; top: -100%; left: 0;
        animation: blink 4s infinite ease-in-out;
    }
    @keyframes eyePulse { 0%, 100% { transform: rotate(45deg) scale(1); filter: brightness(1); } 50% { transform: rotate(45deg) scale(1.1); filter: brightness(1.3); } }
    @keyframes scanning { 0% { top: -10%; } 100% { top: 110%; } }
    @keyframes blink { 0%, 90%, 100% { top: -110%; } 95% { top: 0%; } }

    .report-box { border: 1px solid #00d4ff; padding: 25px; background: rgba(0, 212, 255, 0.05); backdrop-filter: blur(10px); border-radius: 12px; }
    .ad-slot { background: rgba(255, 255, 255, 0.02); border: 1px dashed #333; text-align: center; padding: 15px; margin: 10px 0; color: #444; }
    .trace-text { font-size: 10px; color: #00ff41; opacity: 0.8; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. قاموس اللغات العالمي ---
LANG_MAP = {
    "English": {"title": "SENTINEL OSINT TERMINAL", "scan": "RUN ANALYSIS", "up": "Drop Image", "rtl": False},
    "Spanish": {"title": "TERMINAL SENTINEL", "scan": "EJECUTAR", "up": "Subir Imagen", "rtl": False},
    "Moroccan Darija": {"title": "سنتينل أوسينت تيرمينال", "scan": "حلل الهدف", "up": "حط التصويرة", "rtl": True},
    "French": {"title": "SENTINEL OSINT", "scan": "ANALYSER", "up": "Charger", "rtl": False},
    "Arabic": {"title": "محطة سنتينل الاستخباراتية", "scan": "بدء التحليل", "up": "رفع الصورة", "rtl": True},
    "Russian": {"title": "ТЕРМИНАЛ СЕНТИНЕЛЬ", "scan": "АНАЛИЗ", "up": "Загрузить", "rtl": False},
    "Japanese": {"title": "センチネル OSINT", "scan": "分析実行", "up": "画像をドロップ", "rtl": False}
}

# --- 3. إعداد الـ AI ---
API_KEY = os.environ.get("AI_INTEGRATIONS_GEMINI_API_KEY")
if API_KEY:
    genai.configure(api_key=API_KEY)
    model = genai.GenerativeModel('gemini-1.5-flash') # الإصلاح لـ 404
else:
    st.error("⚠️ AI Key Missing!")

# --- 4. Sidebar (Tools & Trace) ---
with st.sidebar:
    st.markdown("### 🛠️ SYSTEM TOOLS")
    st.checkbox("✅ AI Deep Scan", value=True) #
    st.checkbox("✅ EXIF Extraction", value=True) #
    st.checkbox("✅ Geo-Triangulation", value=True) #
    st.divider()
    selected_lang = st.selectbox("🌐 LANGUAGE", list(LANG_MAP.keys()))
    i18n = LANG_MAP[selected_lang]
    st.divider()
    st.button("💎 UPGRADE TO PRO")
    st.button("💰 Support (Crypto)")
    st.divider()
    st.markdown("### 🌐 DEEP WEB TRACE") #
    st.markdown('<p class="trace-text">Tracing Node: 192.168.1.1...</p>', unsafe_allow_html=True)
    st.markdown('<p class="trace-text">Decrypting Onion Layers...</p>', unsafe_allow_html=True)

# --- 5. الواجهة الرئيسية ---
st.markdown("<div class='ad-slot'>ADSENSE HEADER (728x90)</div>", unsafe_allow_html=True)

# العين اللي كتحرك وتغمض نيشاني
st.markdown('<div class="eye-box"><div class="cyber-eye"></div></div>', unsafe_allow_html=True)
st.markdown(f'<h1 style="text-align: center; color:#00ff41 !important;">{i18n["title"]}</h1>', unsafe_allow_html=True)

# نظام التبويبات (Tabs)
tab1, tab2, tab3 = st.tabs(["📡 SIGNAL SCAN", "🔍 EXIF METADATA", "🌍 GEO-ORBIT"])

with tab1:
    col_input, col_info = st.columns([2, 1])
    with col_input:
        uploaded_file = st.file_uploader(i18n["up"], type=["jpg", "png", "jpeg"])
        if uploaded_file:
            st.image(uploaded_file, caption="Target Identified", use_column_width=True)
            if st.button(i18n["scan"]):
                with st.spinner("Agent Sentinel decoding..."):
                    try:
                        img = Image.open(uploaded_file)
                        response = model.generate_content([img, f"OSINT forensic report in {selected_lang}"])
                        
                        report = response.text
                        if i18n["rtl"]:
                            report = get_display(arabic_reshaper.reshape(report))
                        
                        st.markdown(f'<div class="report-box">{report}</div>', unsafe_allow_html=True)
                        
                        # زر تحميل التقرير
                        pdf = FPDF()
                        pdf.add_page()
                        pdf.set_font("Arial", size=12)
                        pdf.multi_cell(0, 10, txt=response.text.encode('latin-1', 'ignore').decode('latin-1'))
                        st.download_button("📥 DOWNLOAD REPORT", pdf.output(dest='S').encode('latin-1'), "sentinel.pdf")
                    except Exception as e:
                        st.error(f"Scan Failed: {e}")
    with col_info:
        st.markdown("### 🧠 NEURAL ANALYSIS")
        st.info("Waiting for target input...")
        st.markdown("<div class='ad-slot' style='height:300px;'>ADSENSE SIDEBAR</div>", unsafe_allow_html=True)

with tab2:
    st.markdown("### 🔍 RAW METADATA")
    st.write("Upload image to see EXIF data.")

with tab3:
    st.markdown("### 🌍 GEO-TRIANGULATION")
    st.warning("Spatial orbit requires Pro license.")

st.markdown("<div class='ad-slot'>ADSENSE FOOTER</div>", unsafe_allow_html=True)
st.caption("© 2026 Sentinel OSINT v2.5. Ready for AdSense.")
