import streamlit as st
import os
import time
from PIL import Image
from PIL.ExifTags import TAGS
import google.generativeai as genai
import arabic_reshaper
from bidi.algorithm import get_display
from fpdf import FPDF

# --- 1. ثيم Replit الاحترافي (Sentinel Theme) ---
st.set_page_config(page_title="SENTINEL OSINT PRO", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700&display=swap');
    .stApp { background-color: #050505; background-image: radial-gradient(circle at 50% 50%, #001a2e 0%, #050505 100%); color: #00d4ff; font-family: 'JetBrains Mono', monospace; }
    h1, h2, h3, p, span, label { color: #00d4ff !important; text-shadow: 0 0 10px rgba(0, 212, 255, 0.5); }
    .stButton > button { background: linear-gradient(45deg, #00d4ff, #005f73); color: white; border: none; font-weight: bold; width: 100%; box-shadow: 0 4px 15px rgba(0, 212, 255, 0.3); transition: 0.3s; }
    .stButton > button:hover { transform: scale(1.02); box-shadow: 0 0 20px #00d4ff; }
    .report-box { border: 1px solid #00d4ff; padding: 25px; background: rgba(0, 212, 255, 0.05); backdrop-filter: blur(10px); border-radius: 10px; }
    .ad-slot { background: rgba(255, 255, 255, 0.03); border: 1px dashed rgba(0, 212, 255, 0.1); color: #444; text-align: center; padding: 15px; margin: 15px 0; border-radius: 8px; }
    /* Replit Cyber Eye Animation */
    .cyber-eye { width: 100px; height: 100px; background: radial-gradient(circle, #00d4ff 10%, #001a2e 100%); border-radius: 50% 0 50% 0; transform: rotate(45deg); border: 2px solid #00d4ff; margin: 20px auto; animation: eyePulse 4s infinite; }
    @keyframes eyePulse { 0%, 100% { transform: rotate(45deg) scale(1); opacity: 0.8; } 50% { transform: rotate(45deg) scale(1.1); opacity: 1; } }
    </style>
    """, unsafe_allow_html=True)

# --- 2. قاموس اللغات الكامل (بما فيها الإسبانية) ---
LANG_MAP = {
    "English": {"title": "SENTINEL OSINT", "scan": "ANALYZE IMAGE", "rep": "Forensic Report", "up": "Drop Image", "rtl": False, "status": "Operational"},
    "Spanish": {"title": "SENTINEL OSINT", "scan": "EJECUTAR ANÁLISIS", "rep": "Informe Forense", "up": "Subir Imagen", "rtl": False, "status": "Operativo"},
    "Moroccan Darija": {"title": "سنتينل أوسينت", "scan": "حلل التصويرة", "rep": "تقرير جنائي", "up": "حط التصويرة", "rtl": True, "status": "خدّام"},
    "Arabic": {"title": "سنتينل للتحليل", "scan": "بدء التحليل", "rep": "تقرير استخباراتي", "up": "رفع الصورة", "rtl": True, "status": "نشط"},
    "French": {"title": "SENTINEL PRO", "scan": "ANALYSER", "rep": "Rapport Forensique", "up": "Charger", "rtl": False, "status": "Opérationnel"}
}

# --- 3. إعداد الـ AI (Gemini 1.5 Flash) ---
API_KEY = os.environ.get("AI_INTEGRATIONS_GEMINI_API_KEY")
if API_KEY:
    genai.configure(api_key=API_KEY)
    model = genai.GenerativeModel('gemini-1.5-flash')
else:
    st.error("⚠️ AI Key Missing! Please add it to Secrets.")

# --- 4. وظائف تقنية (EXIF & PDF) ---
def get_exif(file):
    try:
        img = Image.open(file)
        exif = img._getexif()
        return {TAGS.get(tag, tag): value for tag, value in exif.items()} if exif else None
    except: return None

# --- 5. واجهة المستخدم ---
st.sidebar.title("🛠️ SYSTEM SETTINGS")
selected_lang = st.sidebar.selectbox("Select Language / لغة", list(LANG_MAP.keys()))
i18n = LANG_MAP[selected_lang]

st.markdown("<div class='ad-slot'>GOOGLE ADSENSE - TOP BANNER</div>", unsafe_allow_html=True)
st.markdown('<div class="cyber-eye"></div>', unsafe_allow_html=True)
st.markdown(f'<h1 style="text-align: center;">{i18n["title"]}</h1>', unsafe_allow_html=True)

col1, col2 = st.columns([3, 1])

with col1:
    uploaded_file = st.file_uploader(i18n["up"], type=["jpg", "jpeg", "png"])
    if uploaded_file:
        img = Image.open(uploaded_file)
        st.image(img, caption="Source Evidence", width=600)
        
        if st.button(i18n["scan"]):
            with st.spinner("Establishing Neural Link..."):
                try:
                    # سحب البيانات المخفية
                    exif_data = get_exif(uploaded_file)
                    # تحليل الذكاء الاصطناعي
                    prompt = f"Act as an OSINT expert. Analyze this image and metadata: {str(exif_data)}. Language: {selected_lang}."
                    response = model.generate_content([img, prompt])
                    
                    st.markdown(f"### 🕵️ {i18n['rep']}")
                    final_text = response.text
                    
                    # دعم العربية والدارجة
                    if i18n["rtl"]:
                        reshaped = arabic_reshaper.reshape(final_text)
                        final_text = get_display(reshaped)
                    
                    st.markdown(f'<div class="report-box">{final_text}</div>', unsafe_allow_html=True)
                    
                    # زر تحميل PDF
                    pdf = FPDF()
                    pdf.add_page()
                    pdf.set_font("Arial", size=12)
                    pdf.multi_cell(0, 10, txt=response.text.encode('latin-1', 'ignore').decode('latin-1'))
                    st.download_button("📥 DOWNLOAD PDF REPORT", pdf.output(dest='S').encode('latin-1'), "sentinel_report.pdf")
                except Exception as e:
                    st.error(f"Analysis Interrupted: {e}")

with col2:
    st.sidebar.success(f"Status: {i18n['status']} 🟢")
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 🌐 NETWORK TRACE")
    st.sidebar.code("Uplink: Secure\nNode: Classified\nEncryption: AES-256")
    st.sidebar.markdown("---")
    st.sidebar.markdown("<div class='ad-slot' style='height: 400px;'>ADSENSE - VERTICAL</div>", unsafe_allow_html=True)

st.markdown("<div class='ad-slot'>GOOGLE ADSENSE - FOOTER</div>", unsafe_allow_html=True)
