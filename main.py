import streamlit as st
import os
import google.generativeai as genai
from PIL import Image
from PIL.ExifTags import TAGS
import pandas as pd
from fpdf import FPDF
import base64

# --- 1. إعدادات النظام والديزاين ---
st.set_page_config(page_title="SENTINEL OSINT PRO", page_icon="🕵️‍♂️", layout="wide")

# CSS لتغيير الألوان لنيون احترافي وأماكن الإعلانات
st.markdown("""
    <style>
    .stApp { background-color: #05070a; color: #00ff41; font-family: 'Courier New', monospace; }
    .ad-slot { background: rgba(0, 255, 65, 0.05); border: 1px dashed #00ff41; text-align: center; padding: 15px; margin: 10px 0; color: #00ff41; font-size: 0.8rem; }
    .stButton>button { border: 1px solid #00ff41; background: transparent; color: #00ff41; width: 100%; font-weight: bold; }
    .stButton>button:hover { background: #00ff41; color: black; box-shadow: 0 0 20px #00ff41; }
    .report-box { border: 1px solid #00ff41; padding: 20px; border-radius: 10px; background: rgba(0, 20, 0, 0.4); }
    </style>
    """, unsafe_allow_html=True)

# --- 2. إعداد الـ AI (Gemini 1.5 Flash) ---
API_KEY = os.environ.get("AI_INTEGRATIONS_GEMINI_API_KEY")
if API_KEY:
    genai.configure(api_key=API_KEY)
    model = genai.GenerativeModel('gemini-1.5-flash')
else:
    st.error("⚠️ CRITICAL ERROR: AI UPLINK DISCONNECTED (Check Secrets)")

# --- 3. الوظائف التقنية (Metadata & PDF) ---
def get_exif_data(img):
    exif_data = {}
    try:
        info = img._getexif()
        if info:
            for tag, value in info.items():
                decoded = TAGS.get(tag, tag)
                exif_data[decoded] = value
    except:
        pass
    return exif_data

def create_pdf_report(analysis_text):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(200, 10, txt="SENTINEL OSINT - FORENSIC REPORT", ln=True, align='C')
    pdf.ln(10)
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, txt=analysis_text)
    return pdf.output(dest='S').encode('latin-1')

# --- 4. الواجهة الرئيسية ---
# إعلان علوي
st.markdown("<div class='ad-slot'>ADSENSE_TOP_LEADERBOARD_728x90</div>", unsafe_allow_html=True)

st.title("🕵️‍♂️ SENTINEL OSINT TERMINAL")
st.markdown("`UPLINK: SECURE` | `LICENSE: PREMIUM` | `CREDITS: 10/10`")

# Sidebar مع إعلان عمودي
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2560/2560243.png", width=80)
    st.markdown("### 🛠️ SYSTEM TOOLS")
    st.checkbox("AI Deep Scan", value=True)
    st.checkbox("EXIF Extraction", value=True)
    st.checkbox("Geo-Triangulation", value=True)
    st.markdown("---")
    st.markdown("<div class='ad-slot' style='height: 400px;'>ADSENSE_SIDEBAR_SKYSCRAPER</div>", unsafe_allow_html=True)
    st.markdown("---")
    if st.button("💰 Support Project (Crypto)"):
        st.info("Wallet: `SENTINEL_OSINT_BTC_ADDRESS`")

# الأقسام الرئيسية (Tabs)
tab1, tab2, tab3 = st.tabs(["📡 SIGNAL SCAN", "🔍 EXIF METADATA", "🌍 GEO-ORBIT"])

with tab1:
    col_input, col_output = st.columns([1, 1.2])
    
    with col_input:
        st.markdown("### 📥 TARGET ACQUISITION")
        uploaded_file = st.file_uploader("Drop file for forensic analysis", type=["jpg", "jpeg", "png"])
        if uploaded_file:
            img = Image.open(uploaded_file)
            st.image(img, caption="TARGET IDENTIFIED", use_column_width=True)
            
    with col_output:
        st.markdown("### 🧠 AI NEURAL ANALYSIS")
        if uploaded_file:
            if st.button("EXECUTE DEEP ANALYSIS"):
                with st.spinner("Agent 'Sentinel' is decoding pixels..."):
                    try:
                        prompt = "Perform a detailed OSINT forensic analysis. Identify: Location clues, object types, image tampering, and possible time of day."
                        response = model.generate_content([img, prompt])
                        analysis_results = response.text
                        
                        st.markdown("<div class='report-box'>", unsafe_allow_html=True)
                        st.markdown(analysis_results)
                        st.markdown("</div>", unsafe_allow_html=True)
                        
                        # زر تحميل التقرير
                        pdf_report = create_pdf_report(analysis_results)
                        st.download_button(
                            label="📥 DOWNLOAD OFFICIAL REPORT (PDF)",
                            data=pdf_report,
                            file_name="Sentinel_Forensic_Report.pdf",
                            mime="application/pdf"
                        )
                    except Exception as e:
                        st.error(f"Analysis Failed: {e}")
        else:
            st.info("Waiting for target input...")

with tab2:
    st.markdown("### 🔍 RAW METADATA EXTRACTION")
    if uploaded_file:
        exif = get_exif_data(img)
        if exif:
            df = pd.DataFrame.from_dict(exif, orient='index', columns=['Value'])
            st.dataframe(df, use_container_width=True)
        else:
            st.warning("NO EXIF HEADERS DETECTED")
    else:
        st.info("Upload an image to see metadata.")

with tab3:
    st.markdown("### 🌍 GEOGRAPHIC TRIANGULATION")
    st.warning("Estimating coordinates based on visual data...")
    st.markdown("`LATITUDE: --.----` | `LONGITUDE: --.----`")
    st.markdown("<div class='ad-slot' style='height: 200px;'>MAP_INTERSTITIAL_AD</div>", unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("<div class='ad-slot'>ADSENSE_FOOTER_BANNER_970x90</div>", unsafe_allow_html=True)
st.caption("© 2026 Sentinel OSINT v2.5. Ready for AdSense.")
