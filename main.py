import streamlit as st
import os
import time
from PIL import Image
from PIL.ExifTags import TAGS
# إصلاح مشكل الـ Import
from google import genai
import arabic_reshaper
from bidi.algorithm import get_display

# --- 1. إعدادات الصفحة والديزاين (Diamond Cyber-UI) ---
st.set_page_config(page_title="SENTINEL OSINT TERMINAL", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700&display=swap');
    .stApp { background-color: #050505; background-image: radial-gradient(circle at 50% 50%, #001a2e 0%, #050505 100%); color: #00d4ff; font-family: 'JetBrains Mono', monospace; }
    
    /* أنيمايشن العين الجوهرة - رمش أفقي وبدون ليزر */
    .eye-container { display: flex; justify-content: center; margin: 30px 0; }
    .cyber-eye {
        width: 100px; height: 100px; 
        background: radial-gradient(circle at 50% 50%, #00d4ff 10%, #001a2e 50%, #050505 100%);
        border-radius: 50% 0 50% 0; transform: rotate(45deg);
        border: 2px solid #00d4ff; box-shadow: 0 0 30px rgba(0, 212, 255, 0.6);
        position: relative; overflow: hidden;
        animation: eyePulse 4s infinite ease-in-out;
    }
    
    /* جفون أفقية (Horizontal Blink) - كيتسدوا من الجناب للوسط */
    .cyber-eye::before, .cyber-eye::after {
        content: ''; position: absolute; width: 0%; height: 100%;
        background: #050505; top: 0; z-index: 5;
        animation: horizontalBlink 5s infinite ease-in-out;
    }
    .cyber-eye::before { left: 0; border-right: 1px solid #00d4ff; }
    .cyber-eye::after { right: 0; border-left: 1px solid #00d4ff; }

    @keyframes eyePulse { 0%, 100% { transform: rotate(45deg) scale(1); } 50% { transform: rotate(45deg) scale(1.08); } }
    @keyframes horizontalBlink { 0%, 90%, 100% { width: 0%; } 95% { width: 55%; } }

    .report-box { border: 1px solid #00d4ff; padding: 25px; background: rgba(0, 212, 255, 0.05); border-radius: 12px; }
    .adsense-box { background: rgba(255, 255, 255, 0.02); border: 1px dashed #333; text-align: center; padding: 15px; margin: 10px 0; color: #444; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. قاموس 10 لغات ---
LANG_MAP = {
    "English": {"title": "SENTINEL OSINT TERMINAL", "up": "Drop Image", "scan": "RUN ANALYSIS", "rtl": False},
    "Moroccan Darija": {"title": "سنتينل أوسينت تيرمينال", "up": "حط التصويرة", "scan": "حلل الهدف", "rtl": True},
    "Arabic": {"title": "محطة سنتينل للاستخبارات", "up": "رفع الصورة", "scan": "بدء المسح", "rtl": True},
    "French": {"title": "TERMINAL SENTINEL", "up": "Charger Target", "scan": "ANALYSER", "rtl": False},
    "Spanish": {"title": "TERMINAL SENTINEL", "up": "Subir Imagen", "scan": "EJECUTAR", "rtl": False},
    "German": {"title": "SENTINEL TERMINAL", "up": "Bild hochladen", "scan": "STARTEN", "rtl": False},
    "Russian": {"title": "ТЕРМИНАЛ СЕНТИНЕЛЬ", "up": "Загрузить", "scan": "АНАЛИЗ", "rtl": False},
    "Chinese": {"title": "哨兵 OSINT 終端", "up": "目標獲取", "scan": "掃描", "rtl": False},
    "Japanese": {"title": "センチネル OSINT", "up": "アップロード", "scan": "実行", "rtl": False},
    "Turkish": {"title": "SENTINEL TERMİNALİ", "up": "Yükle", "scan": "ANALİZ", "rtl": False}
}

# --- 3. إصلاح الـ API (حل مشكل 404) ---
AI_KEY = os.environ.get("AI_INTEGRATIONS_GEMINI_API_KEY")
AI_URL = os.environ.get("AI_INTEGRATIONS_GEMINI_BASE_URL")

client = genai.Client(
    api_key=AI_KEY,
    http_options={'api_version': 'v1beta', 'base_url': AI_URL}
)

# --- 4. Sidebar (الأدوات التلاتة الأصلية) ---
with st.sidebar:
    st.markdown("### 🛠️ SYSTEM TOOLS")
    st.checkbox("✅ AI Deep Scan", value=True)
    st.checkbox("✅ EXIF Extraction", value=True)
    st.checkbox("✅ Geo-Triangulation", value=True)
    st.divider()
    selected_lang = st.selectbox("🌐 LANGUAGE", list(LANG_MAP.keys()))
    i18n = LANG_MAP[selected_lang]
    st.divider()
    st.button("💎 UPGRADE TO PRO")
    st.button("💰 Support Project (Crypto)")

# --- 5. الصفحة الرئيسية ---
st.markdown("<div class='adsense-box'>Google AdSense - Header Banner</div>", unsafe_allow_html=True)

# العين الجوهرة الأصلية بالرمش الأفقي
st.markdown('<div class="eye-container"><div class="cyber-eye"></div></div>', unsafe_allow_html=True)
st.markdown(f'<h1 style="text-align: center; color: #00ff41 !important;">{i18n["title"]}</h1>', unsafe_allow_html=True)

# التبويبات (Signal, Metadata, Geo)
tab1, tab2, tab3 = st.tabs(["📡 SIGNAL SCAN", "🔍 EXIF METADATA", "🌍 GEO-ORBIT"])

with tab1:
    col_l, col_r = st.columns([2, 1])
    with col_l:
        uploaded_file = st.file_uploader(i18n["up"], type=["jpg", "png", "jpeg"])
        if uploaded_file:
            st.image(uploaded_file, caption="Target Acquired", width=500)
            if st.button(i18n["scan"]):
                with st.spinner("Decoding pixels..."):
                    try:
                        # تصحيح الموديل لـ gemini-1.5-flash لحل مشكل 404
                        response = client.models.generate_content(
                            model="gemini-1.5-flash",
                            contents=[f"Deep OSINT report in {selected_lang}", uploaded_file]
                        )
                        report = response.text
                        if i18n["rtl"]:
                            report = get_display(arabic_reshaper.reshape(report))
                        st.markdown(f'<div class="report-box">{report}</div>', unsafe_allow_html=True)
                    except Exception as e:
                        st.error(f"Analysis Error: {e}")
    with col_r:
        st.markdown("### 🧠 AI ANALYSIS")
        st.info("System Ready for Target.")
        st.markdown("<div class='adsense-box' style='height:300px;'>Vertical Ad</div>", unsafe_allow_html=True)

st.markdown("<div class='adsense-box'>Google AdSense - Footer Banner</div>", unsafe_allow_html=True)
st.caption("© 2026 Sentinel OSINT v2.5 | Powering by Gemini AI")
