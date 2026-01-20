import streamlit as st
import os
import time
from PIL import Image
from PIL.ExifTags import TAGS
# إصلاح مشكل الـ Import اللي بان فالتصاور
try:
    import google.generativeai as genai
except ImportError:
    st.error("Install library: pip install google-generativeai")

import arabic_reshaper
from bidi.algorithm import get_display

# --- 1. ثيم SENTINEL الجوهرة (Cyber-UI) ---
st.set_page_config(page_title="SENTINEL OSINT TERMINAL", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700&display=swap');
    .stApp { background-color: #050505; background-image: radial-gradient(circle at 50% 50%, #001a2e 0%, #050505 100%); color: #00d4ff; font-family: 'JetBrains Mono', monospace; }
    
    /* أنيمايشن العين الجوهرة الأصلية - رمش أفقي */
    .eye-container { display: flex; justify-content: center; margin: 30px 0; }
    .cyber-eye {
        width: 100px; height: 100px; 
        background: radial-gradient(circle at 50% 50%, #00d4ff 10%, #001a2e 50%, #050505 100%);
        border-radius: 50% 0 50% 0; transform: rotate(45deg);
        border: 2px solid #00d4ff; box-shadow: 0 0 30px rgba(0, 212, 255, 0.6);
        position: relative; overflow: hidden;
        animation: eyePulse 4s infinite ease-in-out;
    }
    /* جفون أفقية كتسد من الجناب (بدون ليزر) */
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
    .ads-box { background: rgba(255, 255, 255, 0.02); border: 1px dashed #333; text-align: center; padding: 15px; color: #444; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. إعداد الـ API (إصلاح 404) ---
API_KEY = os.environ.get("AI_INTEGRATIONS_GEMINI_API_KEY")
genai.configure(api_key=API_KEY)

# --- 3. الأدوات واللغات (Sidebar) ---
with st.sidebar:
    st.markdown("### 🛠️ SYSTEM TOOLS")
    st.checkbox("✅ AI Deep Scan", value=True)
    st.checkbox("✅ EXIF Extraction", value=True)
    st.checkbox("✅ Geo-Triangulation", value=True)
    st.divider()
    lang = st.selectbox("🌐 LANGUAGE", ["English", "Moroccan Darija", "French", "Spanish", "Arabic", "Russian", "Chinese", "Japanese", "Turkish", "German"])
    st.divider()
    st.button("💎 UPGRADE TO PRO")
    st.button("💰 Support Project (Crypto)")

# --- 4. الواجهة الرئيسية ---
st.markdown("<div class='ads-box'>ADSENSE HEADER</div>", unsafe_allow_html=True)
st.markdown('<div class="eye-container"><div class="cyber-eye"></div></div>', unsafe_allow_html=True)
st.markdown(f'<h1 style="text-align: center; color: #00ff41 !important;">SENTINEL OSINT TERMINAL</h1>', unsafe_allow_html=True)

tab1, tab2, tab3 = st.tabs(["📡 SIGNAL SCAN", "🔍 EXIF METADATA", "🌍 GEO-ORBIT"])

with tab1:
    col_l, col_r = st.columns([2, 1])
    with col_l:
        up = st.file_uploader("Drop target image", type=["jpg", "png", "jpeg"])
        if up:
            st.image(up, width=500)
            if st.button("RUN ANALYSIS"):
                with st.spinner("Decoding..."):
                    try:
                        # تبديل الموديل لـ 1.5-flash لضمان الخدمة
                        model = genai.GenerativeModel('gemini-1.5-flash')
                        img = Image.open(up)
                        response = model.generate_content([f"Deep OSINT forensic report in {lang}", img])
                        st.markdown(f'<div class="report-box">{response.text}</div>', unsafe_allow_html=True)
                    except Exception as e:
                        st.error(f"Error: {e}")
    with col_r:
        st.markdown("### 🧠 AI NEURAL")
        st.info("System Ready.")
        st.markdown("<div class='ads-box' style='height:250px;'>SIDE AD</div>", unsafe_allow_html=True)

st.markdown("<div class='ads-box'>ADSENSE FOOTER</div>", unsafe_allow_html=True)
st.caption("© 2026 Sentinel OSINT v2.5. Ready for Monetization.")
