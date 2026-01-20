import streamlit as st
import os
import google.generativeai as genai
import arabic_reshaper
from bidi.algorithm import get_display
from fpdf import FPDF
import pandas as pd
from PIL import Image

# --- Config ---
st.set_page_config(page_title="Sentinel OSINT", layout="wide")

# --- API Setup ---
API_KEY = os.environ.get("AI_INTEGRATIONS_GEMINI_API_KEY")

if API_KEY:
    genai.configure(api_key=API_KEY)
   model = genai.GenerativeModel('gemini-1.5-flash')
else:
    st.warning("Please add AI_INTEGRATIONS_GEMINI_API_KEY to Secrets.")

# --- Interface ---
st.title("SENTINEL OSINT")
st.subheader("FORENSIC IMAGE INTELLIGENCE & ANALYSIS")

uploaded_file = st.file_uploader("Drop image for forensic analysis", type=["jpg", "jpeg", "png"])

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="Target Image", use_column_width=True)
    
    if st.button("Analyze Image"):
        if not API_KEY:
            st.error("API Key missing!")
        else:
            try:
                response = model.generate_content([image, "Perform a detailed forensic analysis on this image."])
                st.markdown("### Analysis Results:")
                st.write(response.text)
            except Exception as e:
                st.error(f"Error: {e}")
