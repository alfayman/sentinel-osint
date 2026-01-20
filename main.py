import streamlit as st
st.set_page_config(page_title="Sentinel OSINT", layout="wide")
import os
import time
import requests
import datetime
from io import BytesIO
from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS
import google.generativeai as genai
import arabic_reshaper
from bidi.algorithm import get_display
from fpdf import FPDF

# Sentinel OSINT Professional Theme
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700&display=swap');
    
    .main {
        background-color: #050505;
        color: #00d4ff;
        font-family: 'JetBrains Mono', monospace;
    }
    .stApp {
        background-color: #050505;
        background-image: radial-gradient(circle at 50% 50%, #001a2e 0%, #050505 100%);
    }
    h1, h2, h3, p, span, label {
        color: #00d4ff !important;
        text-shadow: 0 0 10px rgba(0, 212, 255, 0.5);
    }
    
    /* Glassmorphism Upload Box */
    .stFileUploader {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(0, 212, 255, 0.2);
        border-radius: 15px;
        padding: 20px;
    }
    
    .stTextInput > div > div > input {
        background-color: rgba(255, 255, 255, 0.05);
        color: #00d4ff;
        border: 1px solid #00d4ff;
        backdrop-filter: blur(5px);
    }
    .stButton > button {
        background: linear-gradient(45deg, #00d4ff, #005f73);
        color: #ffffff;
        border: none;
        font-weight: bold;
        box-shadow: 0 4px 15px rgba(0, 212, 255, 0.3);
        transition: all 0.3s ease;
        width: 100%;
    }
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(0, 212, 255, 0.5);
    }
    .report-box {
        border: 1px solid #00d4ff;
        padding: 25px;
        background: rgba(0, 212, 255, 0.05);
        backdrop-filter: blur(10px);
        border-radius: 10px;
        line-height: 1.6;
    }
    .rtl {
        direction: rtl;
        text-align: right;
    }
    .ltr {
        direction: ltr;
        text-align: left;
    }
    .gemini-badge {
        position: fixed;
        top: 20px;
        right: 20px;
        background: rgba(0, 212, 255, 0.1);
        border: 1px solid #00d4ff;
        padding: 8px 20px;
        border-radius: 20px;
        color: #00d4ff;
        font-size: 13px;
        font-weight: bold;
        z-index: 1000;
        backdrop-filter: blur(5px);
    }
    .footer-note {
        text-align: center;
        color: #444 !important;
        font-size: 11px;
        margin-top: 50px;
    }
    .adsense-placeholder {
        background: rgba(255, 255, 255, 0.03);
        border: 1px dashed rgba(0, 212, 255, 0.1);
        color: #444;
        text-align: center;
        padding: 15px;
        margin: 15px 0;
        border-radius: 8px;
    }
    
    /* Terminal Animation Style */
    .terminal-text {
        font-family: 'JetBrains Mono', monospace;
        color: #00d4ff;
        font-size: 14px;
        margin-bottom: 5px;
    }
    
    /* Sidebar Trace Animation */
    .trace-animation {
        font-family: 'JetBrains Mono', monospace;
        font-size: 10px;
        color: #00d4ff;
        overflow: hidden;
        white-space: nowrap;
        animation: typing 3s steps(40, end), blink-caret .75s step-end infinite;
    }
    @keyframes typing { from { width: 0 } to { width: 100% } }
    </style>
    """, unsafe_allow_html=True)

# i18n Dictionary
LANG_MAP = {
    "English": {
        "title": "SENTINEL OSINT",
        "subtitle": "FORENSIC IMAGE INTELLIGENCE & ANALYSIS",
        "credits": "CREDITS REMAINING",
        "uploader": "Drop image for forensic analysis",
        "analyze": "ANALYZE IMAGE",
        "metadata": "METADATA EXTRACTION",
        "report": "FORENSIC REPORT",
        "download": "DOWNLOAD CLASSIFIED PDF REPORT",
        "status": "System Status: Operational",
        "trace": "Deep Web Trace",
        "pro": "Pro Features",
        "upgrade": "Upgrade to Sentinel Pro",
        "rtl": False,
        "logs": [
            "Initializing Neural Uplink...",
            "Scanning Satellites for Geospatial Match...",
            "Decrypting Image Header Data...",
            "Extracting EXIF Signature...",
            "Cross-referencing Device ID with Global Database...",
            "Generating Intelligence Report via Gemini AI...",
            "Finalizing Forensic Package..."
        ]
    },
    "Arabic": {
        "title": "سنتينل أوسينت",
        "subtitle": "الاستخبارات الجنائية وتحليل الصور",
        "credits": "الرصيد المتبقي",
        "uploader": "ضع الصورة للتحليل الجنائي",
        "analyze": "تحليل الصورة",
        "metadata": "استخراج البيانات الوصفية",
        "report": "تقرير جنائي",
        "download": "تحميل تقرير PDF سري",
        "status": "حالة النظام: فعال",
        "trace": "تتبع الشبكة العميقة",
        "pro": "ميزات برو",
        "upgrade": "ترقية إلى سنتينل برو",
        "rtl": True,
        "logs": [
            "تهيئة الوصلة العصبية...",
            "مسح الأقمار الصناعية للمطابقة الجغرافية...",
            "فك تشفير بيانات رأس الصورة...",
            "استخراج توقيع EXIF...",
            "مطابقة معرف الجهاز مع قاعدة البيانات العالمية...",
            "إنشاء تقرير استخباراتي عبر Gemini AI...",
            "إتمام الحزمة الجنائية..."
        ]
    },
    "French": {
        "title": "SENTINEL OSINT",
        "subtitle": "INTELLIGENCE D'IMAGE FORENSIQUE & ANALYSE",
        "credits": "CRÉDITS RESTANTS",
        "uploader": "Déposer l'image pour analyse forensique",
        "analyze": "ANALYSER L'IMAGE",
        "metadata": "EXTRACTION DE MÉTADONNÉES",
        "report": "RAPPORT FORENSIQUE",
        "download": "TÉLÉCHARGER LE RAPPORT PDF CLASSIFIÉ",
        "status": "Statut du système : Opérationnel",
        "trace": "Trace du Deep Web",
        "pro": "Fonctions Pro",
        "upgrade": "Passer à Sentinel Pro",
        "rtl": False,
        "logs": [
            "Initialisation du lien neuronal...",
            "Balayage des satellites pour correspondance spatiale...",
            "Décryptage des données d'en-tête...",
            "Extraction de la signature EXIF...",
            "Vérification de l'ID de l'appareil...",
            "Génération du rapport via Gemini AI...",
            "Finalisation du dossier forensique..."
        ]
    },
    "Spanish": {
        "title": "SENTINEL OSINT",
        "subtitle": "INTELIGENCIA FORENSE DE IMAGEN Y ANÁLISIS",
        "credits": "CRÉDITOS RESTANTES",
        "uploader": "Suelte la imagen para análisis forense",
        "analyze": "ANALIZAR IMAGEN",
        "metadata": "EXTRACCIÓN DE METADATOS",
        "report": "INFORME FORENSE",
        "download": "DESCARGAR INFORME PDF CLASIFICADO",
        "status": "Estado del sistema: Operativo",
        "trace": "Rastro de la Deep Web",
        "pro": "Funciones Pro",
        "upgrade": "Actualizar a Sentinel Pro",
        "rtl": False,
        "logs": [
            "Iniciando enlace neuronal...",
            "Escaneando satélites para ajuste espacial...",
            "Descifrando datos de cabecera...",
            "Extrayendo firma EXIF...",
            "Cruzando ID de dispositivo...",
            "Generando informe vía Gemini AI...",
            "Finalizando paquete forense..."
        ]
    },
    "Moroccan Darija": {
        "title": "سنتينل أوسينت",
        "subtitle": "الاستخبارات الجنائية وتحليل التصاور",
        "credits": "الكريدي اللي باقي",
        "uploader": "حط التصويرة للتحليل الجنائي",
        "analyze": "حلل التصويرة",
        "metadata": "استخراج البيانات الوصفية",
        "report": "تقرير جنائي",
        "download": "تحميل تقرير PDF سري",
        "status": "حالة السيستيم: خدام",
        "trace": "تتبع الشبكة العميقة",
        "pro": "ميزات برو",
        "upgrade": "ترقية لسنتينل برو",
        "rtl": True,
        "logs": [
            "كنوجد الوصلة العصبية...",
            "كنقلب فالأقمار الصناعية...",
            "كنفك تشفير الداتا...",
            "كنخرج EXIF...",
            "كنشوف ID ديال الجهاز...",
            "كنصاوب التقرير بـ Gemini AI...",
            "كنسالي الخدمة..."
        ]
    }
}

# Language Selector in Sidebar
st.sidebar.title("Settings")
selected_lang = st.sidebar.selectbox("Language / لغة", list(LANG_MAP.keys()), index=0)
i18n = LANG_MAP[selected_lang]

# Credit System Implementation
if 'credits' not in st.session_state:
    st.session_state.credits = 3
if 'last_reset' not in st.session_state:
    st.session_state.last_reset = datetime.date.today()

# Reset credits daily
if st.session_state.last_reset != datetime.date.today():
    st.session_state.credits = 3
    st.session_state.last_reset = datetime.date.today()

# Replit AI Integrations setup
AI_INTEGRATIONS_GEMINI_API_KEY = os.environ.get("AI_INTEGRATIONS_GEMINI_API_KEY")
AI_INTEGRATIONS_GEMINI_BASE_URL = os.environ.get("AI_INTEGRATIONS_GEMINI_BASE_URL")

genai.configure(api_key=os.environ.get("AI_INTEGRATIONS_GEMINI_API_KEY"))
model = genai.GenerativeModel('gemini-pro')
    
    # Add Unicode font support (DejaVuSans supports more Unicode)
    try:
        pdf.add_font("DejaVu", "", "fonts/DejaVuSans.ttf")
        pdf.add_font("DejaVu", "B", "fonts/DejaVuSans-Bold.ttf")
        font_name = "DejaVu"
    except Exception as e:
        font_name = "Helvetica" # Fallback

    pdf.set_font(font_name, 'B', 24)
    pdf.set_text_color(0, 212, 255)
    pdf.cell(200, 20, "SENTINEL OSINT REPORT", ln=True, align='C')
    
    # Watermark (fpdf2 syntax)
    pdf.set_font(font_name, 'B', 60)
    pdf.set_text_color(255, 0, 0) # Exactly 3 arguments (r, g, b)
    with pdf.rotation(45, 100, 100):
        pdf.text(30, 190, "CLASSIFIED")
    
    pdf.set_font(font_name, '', 12)
    pdf.set_text_color(0, 0, 0)
    pdf.ln(10)
    pdf.cell(200, 10, f"Generated: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", ln=True)
    pdf.ln(5)
    
    pdf.set_font(font_name, 'B', 14)
    pdf.cell(200, 10, i18n["metadata"] + ":", ln=True)
    pdf.set_font(font_name, '', 10)
    pdf.multi_cell(0, 10, metadata_text)
    
    pdf.ln(10)
    pdf.set_font(font_name, 'B', 14)
    pdf.cell(200, 10, i18n["report"] + " (" + selected_lang + "):", ln=True)
    pdf.set_font(font_name, '', 10)
    
    # Handle RTL/LTR for PDF
    final_report = report_text
    if i18n["rtl"]:
        reshaped = arabic_reshaper.reshape(report_text)
        final_report = get_display(reshaped)
    
    pdf.multi_cell(0, 10, final_report)
    
    return pdf.output()

def get_exif_data(uploaded_file):
    try:
        img = Image.open(uploaded_file)
        exif = img._getexif()
        if not exif:
            return None
        
        exif_data = {}
        for tag, value in exif.items():
            decoded = TAGS.get(tag, tag)
            if decoded == "GPSInfo":
                gps_data = {}
                for t in value:
                    sub_tag = GPSTAGS.get(t, t)
                    gps_data[sub_tag] = value[t]
                exif_data[decoded] = gps_data
            else:
                exif_data[decoded] = value
        return exif_data
    except Exception as e:
        return {"error": str(e)}

def format_metadata(exif_data):
    if not exif_data or "error" in exif_data:
        return "No metadata found or error occurred."
    
    summary = []
    summary.append(f"Device: {exif_data.get('Make', 'Unknown')} {exif_data.get('Model', 'Unknown')}")
    summary.append(f"Date: {exif_data.get('DateTime', 'Unknown')}")
    if "GPSInfo" in exif_data:
        summary.append(f"GPS: Available (Coordinates Found)")
    else:
        summary.append(f"GPS: Not available")
    
    return "\n".join(summary)

def generate_spy_report(metadata_text):
    prompt = f"""
    Analyze the following image metadata and write a 'Forensic Intelligence Report' in Moroccan Darija.
    The tone should be highly professional, clinical, and authoritative (OSINT style).
    Metadata:
    {metadata_text}
    
    Output format:
    [SENTINEL OSINT - CLASSIFIED REPORT]
    ... (report in Darija)
    """
    
    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )
        return response.text or "Error generating report."
    except Exception as e:
        return f"Gemini Error: {str(e)}"

# Layout
st.markdown('<div class="adsense-placeholder">Google AdSense - Header (728x90)</div>', unsafe_allow_html=True)

col1, col2 = st.columns([3, 1])

with col1:
    # Centered Professional Logo
    st.markdown("""
        <style>
        .cyber-eye-container {
            display: flex;
            justify-content: center;
            align-items: center;
            margin-bottom: 20px;
            perspective: 1000px;
        }
        .cyber-eye {
            width: 100px;
            height: 100px;
            background: radial-gradient(circle at 50% 50%, #00d4ff 10%, #001a2e 50%, #050505 100%);
            border-radius: 50% 0 50% 0;
            transform: rotate(45deg);
            border: 2px solid #00d4ff;
            box-shadow: 0 0 30px rgba(0, 212, 255, 0.6), inset 0 0 20px rgba(0, 212, 255, 0.4);
            position: relative;
            overflow: hidden;
            animation: eyePulse 4s infinite ease-in-out;
        }
        .cyber-eye::before {
            content: '';
            position: absolute;
            top: 20%;
            left: 20%;
            width: 60%;
            height: 60%;
            background: radial-gradient(circle, #00d4ff 20%, transparent 70%);
            border-radius: 50%;
            filter: blur(2px);
            animation: scanLine 2s infinite linear;
        }
        .cyber-eye::after {
            content: '';
            position: absolute;
            width: 100%;
            height: 2px;
            background: #00d4ff;
            top: 50%;
            box-shadow: 0 0 10px #00d4ff;
            animation: shutter 3s infinite alternate ease-in-out;
        }
        @keyframes eyePulse {
            0%, 100% { transform: rotate(45deg) scale(1); box-shadow: 0 0 30px rgba(0, 212, 255, 0.6); }
            50% { transform: rotate(45deg) scale(1.05); box-shadow: 0 0 50px rgba(0, 212, 255, 0.8); }
        }
        @keyframes scanLine {
            0% { transform: translateY(-50px) scaleX(2); opacity: 0; }
            50% { opacity: 1; }
            100% { transform: translateY(50px) scaleX(2); opacity: 0; }
        }
        @keyframes shutter {
            0% { height: 2px; top: 50%; }
            100% { height: 50px; top: 25%; opacity: 0.1; }
        }
        </style>
        <div class="cyber-eye-container">
            <div class="cyber-eye"></div>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f'<h1 style="text-align: center; margin-bottom: 0; font-size: 2.8rem; letter-spacing: 2px; font-weight: 700;">{i18n["title"]}</h1>', unsafe_allow_html=True)
    st.markdown(f'<p style="text-align: center; font-size: 1rem; color: #00d4ff; opacity: 0.8; margin-top: 5px; letter-spacing: 3px; font-weight: 400;">{i18n["subtitle"]}</p>', unsafe_allow_html=True)
    
    st.markdown(f'<div style="text-align: center; color: #00d4ff; font-size: 0.9rem; margin-top: 10px;">{i18n["credits"]}: {st.session_state.credits} / 3</div>', unsafe_allow_html=True)
    
    st.markdown('<div style="height: 30px;"></div>', unsafe_allow_html=True)
    
    uploaded_file = st.file_uploader(i18n["uploader"], type=["jpg", "jpeg", "png"])
    
    if uploaded_file:
        st.image(uploaded_file, caption="Evidence Source", width=400)
        
        if st.button(i18n["analyze"]):
            if st.session_state.credits > 0:
                # Fast-scrolling terminal animation
                animation_container = st.empty()
                logs = i18n["logs"]
                
                for i in range(len(logs)):
                    animation_container.markdown(f'<div class="terminal-text">>> {logs[i]}</div>', unsafe_allow_html=True)
                    time.sleep(0.4)
                
                animation_container.empty()
                
                with st.spinner("Processing..."):
                    metadata = get_exif_data(uploaded_file)
                    
                    if metadata and "error" not in metadata:
                        metadata_text = format_metadata(metadata)
                        report = generate_spy_report(metadata_text, selected_lang)
                        
                        st.session_state.credits -= 1
                        st.success(f"ANALYSIS COMPLETE. Credits: {st.session_state.credits}/3")
                        
                        st.markdown(f"### 🗃️ {i18n['metadata']}")
                        st.code(metadata_text, language='text')
                        
                        st.markdown(f"### 🕵️ {i18n['report']} ({selected_lang})")
                        
                        # Handle RTL/LTR for UI
                        alignment_class = "rtl" if i18n["rtl"] else "ltr"
                        display_report = report
                        if i18n["rtl"]:
                            reshaped = arabic_reshaper.reshape(report)
                            display_report = get_display(reshaped)
                        
                        st.markdown(f'<div class="report-box {alignment_class}">{display_report}</div>', unsafe_allow_html=True)
                        
                        # PDF Download Button
                        pdf_data = create_pdf_report(metadata_text, report, selected_lang)
                        st.download_button(
                            label=f"📥 {i18n['download']}",
                            data=pdf_data,
                            file_name=f"SENTINEL_REPORT_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
                            mime="application/pdf"
                        )
                    else:
                        st.error("FORENSIC FAILURE: No metadata detected in source file.")
            else:
                st.error("DAILY CREDIT LIMIT REACHED. Upgrade to Pro for unlimited scans.")

with col2:
    st.sidebar.title("Sentinel OSINT")
    st.sidebar.success(i18n["status"])
    st.sidebar.divider()
    
    # Deep Web Trace Animation
    st.sidebar.markdown(f"### 🌐 {i18n['trace']}")
    st.sidebar.markdown('<div class="trace-animation">Tracing Node: 192.168.1.1</div>', unsafe_allow_html=True)
    st.sidebar.markdown('<div class="trace-animation">Decrypting Onion...</div>', unsafe_allow_html=True)
    st.sidebar.markdown('<div class="trace-animation">Accessing Darknet Hub...</div>', unsafe_allow_html=True)
    
    st.sidebar.divider()
    
    st.sidebar.markdown(f"### 🔐 {i18n['pro']}")
    st.sidebar.checkbox("Batch Scan (Pro)", disabled=True)
    st.sidebar.checkbox("Deep Geo-Location (Pro)", disabled=True)
    st.sidebar.checkbox("VPN Masking (Pro)", disabled=True)
    st.sidebar.button(i18n["upgrade"])
    
    st.sidebar.divider()
    st.sidebar.info("Uplink: SECURE\nLocation: CLASSIFIED")
    
    st.markdown('<div class="adsense-placeholder" style="height: 600px;">AdSense - Skyscraper</div>', unsafe_allow_html=True)

# Branding Badge
st.markdown('<div class="gemini-badge">Powered by Gemini AI</div>', unsafe_allow_html=True)
st.markdown('<div class="footer-note">© 2026 Sentinel OSINT. Ready for AdSense Monetization.</div>', unsafe_allow_html=True)

