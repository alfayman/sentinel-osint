import streamlit as st
import os
import time
from PIL import Image
from PIL.ExifTags import TAGS
import google.generativeai as genai
import arabic_reshaper
from bidi.algorithm import get_display
from fpdf import FPDF

# --- 1. ثيم الـ Biometric Sentinel (Realistic & Professional) ---
st.set_page_config(page_title="SENTINEL OSINT PRO", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700&display=swap');
    .stApp { background-color: #050505; background-image: radial-gradient(circle at 50% 50%, #001a2e 0%, #050505 100%); color: #00d4ff; font-family: 'JetBrains Mono', monospace; }
    
    /* أنيمايشن العين الواقعية (Biometric Realistic Eye) */
    .eye-wrapper { display: flex; justify-content: center; margin: 40px 0; }
    .realistic-eye {
        width: 150px; height: 150px;
        background: white;
        border-radius: 75% 10%; /* شكل العين الواقعي */
        transform: rotate(45deg);
        position: relative;
        overflow: hidden;
        border: 4px solid #00d4ff;
        box-shadow: 0 0 40px rgba(0, 212, 255, 0.6), inset 0 0 20px #000;
        display: flex; justify-content: center; align-items: center;
    }
    .iris {
        width: 80px; height: 80px;
        background: radial-gradient(circle, #001a2e 10%, #00d4ff 40%, #005f73 70%, #000 100%);
        border-radius: 50%;
        display: flex; justify-content: center; align-items: center;
        border: 2px solid rgba(0, 212, 255, 0.5);
        animation: rotateIris 10s infinite linear;
    }
    .pupil {
        width: 30px; height: 30px;
        background: #000;
        border-radius: 50%;
        box-shadow: 0 0 10px #000;
        animation: pupilPulse 4s infinite ease-in-out;
    }
    /* جفون أفقية واقعية */
    .eyelid-l, .eyelid-r {
        position: absolute; width: 0%; height: 100%;
        background: #050505; z-index: 10;
        animation: horizontalBlink 6s infinite ease-in-out;
    }
    .eyelid-l { left: 0; border-right: 1px solid #00d4ff; }
    .eyelid-r { right: 0; border-left: 1px solid #00d4ff; }

    @keyframes pupilPulse { 0%, 100% { transform: scale(1); } 50% { transform: scale(1.3); } }
    @keyframes rotateIris { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }
    @keyframes horizontalBlink { 0%, 90%, 100% { width: 0%; } 95% { width: 52%; } }

    .report-box { border: 1px solid #00d4ff; padding: 25px; background: rgba(0, 212, 255, 0.05); border-radius: 15px; }
    .ad-slot { background: rgba(255, 255, 255, 0.02); border: 1px dashed rgba(0, 212, 255, 0.2); text-align: center; padding: 15px; margin: 15px 0; color: #444; border-radius: 8px; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. اللغات الشاملة ---
LANG_MAP = {
    "English": {"title": "SENTINEL BIOMETRIC OSINT", "scan": "EXECUTE ANALYSIS", "up": "Drop Image", "rtl": False},
    "Moroccan Darija": {"title": "سنتينل للتحليل البصري", "scan": "حلل الهدف", "up": "حط التصويرة", "rtl": True},
    "Spanish": {"title": "SENTINEL OSINT PRO", "scan": "EJECUTAR", "up": "Subir Imagen", "rtl": False},
    "French": {"title": "SENTINEL OSINT", "scan": "ANALYSER", "up": "Charger Target", "rtl": False},
    "Arabic": {"title": "محطة سنتينل للاستخبارات", "scan": "بدء التحليل", "up": "رفع الصورة", "rtl": True},
    "Russian": {"title": "СЕНТИНЕЛЬ ОСИНТ", "scan": "АНАЛИЗ", "up": "Загрузить", "rtl": False},
    "Japanese": {"title": "センチネル OSINT", "scan": "分析実行", "up": "画像アップロード", "rtl": False}
}

# --- 3. إعداد الـ AI ---
API_KEY = os.environ.get("AI_INTEGRATIONS_GEMINI_API_KEY")
if API_KEY:
    genai.configure(api_key=API_KEY)
    model = genai.GenerativeModel('gemini-1.5-flash')
else:
    st.error("⚠️ AI Link Offline - Check Key")

# --- 4. Sidebar (الأدوات الاحترافية) ---
with st.sidebar:
    st.markdown("### 🛠️ CORE TOOLS")
    st.checkbox("✅ AI Neural Scan", value=True)
    st.checkbox("✅ EXIF Forensic", value=True)
    st.checkbox("✅ Geo-Triangulation", value=True)
    st.divider()
    selected_lang = st.selectbox("🌐 INTERFACE LANGUAGE", list(LANG_MAP.keys()))
    i18n = LANG_MAP[selected_lang]
    st.divider()
    st.button("🚀 UPGRADE TO PRO")
    st.button("💰 Support Project")
    st.divider()
    st.markdown("### 📡 SYSTEM STATUS")
    st.code("Uplink: STABLE\nNode: CLASSIFIED\nClearance: LEVEL 5")

# --- 5. الصفحة الرئيسية ---
st.markdown("<div class='ad-slot'>GOOGLE ADSENSE - TOP BANNER</div>", unsafe_allow_html=True)

# العين الواقعية (The Biometric Eye)
st.markdown("""
<div class='eye-wrapper'>
    <div class='realistic-eye'>
        <div class='eyelid-l'></div>
        <div class='eyelid-r'></div>
        <div class='iris'>
            <div class='pupil'></div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown(f'<h1 style="text-align: center; color: #00ff41 !important;">{i18n["title"]}</h1>', unsafe_allow_html=True)

tab1, tab2, tab3 = st.tabs(["📡 SIGNAL SCAN", "🔍 EXIF HEADERS", "🌍 GEO-ORBIT"])

with tab1:
    col_l, col_r = st.columns([2, 1])
    with col_l:
        uploaded_file = st.file_uploader(i18n["up"], type=["jpg", "png", "jpeg"])
        if uploaded_file:
            st.image(uploaded_file, caption="IDENTIFIED TARGET", use_column_width=True)
            if st.button(i18n["scan"]):
                with st.spinner("Analyzing biometric patterns..."):
                    try:
                        img = Image.open(uploaded_file)
                        response = model.generate_content([img, f"Professional OSINT forensic report in {selected_lang}."])
                        report = response.text
                        if i18n["rtl"]:
                            report = get_display(arabic_reshaper.reshape(report))
                        st.markdown(f'<div class="report-box">{report}</div>', unsafe_allow_html=True)
                    except Exception as e:
                        st.error(f"Error: {e}")
    with col_r:
        st.markdown("### 🧠 AI ENGINE")
        st.info("Agent Sentinel is Ready.")
        st.markdown("<div class='ad-slot' style='height:400px;'>AdSense Vertical Ad</div>", unsafe_allow_html=True)

st.markdown("<div class='ad-slot'>GOOGLE ADSENSE - FOOTER BANNER</div>", unsafe_allow_html=True)
