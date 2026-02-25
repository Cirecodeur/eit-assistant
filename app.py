import streamlit as st
import google.generativeai as genai
import requests
from bs4 import BeautifulSoup
import PyPDF2
import logging
import os
from dotenv import load_dotenv
from fpdf import FPDF

# 1. LOGGING CONFIGURATION (Critère : It should have logs)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("app.log"), # Writes to a file
        logging.StreamHandler()         # Also shows in console for Fly.io
    ]
)
logger = logging.getLogger(__name__)

load_dotenv()
ASSISTANT_NAME = "Eric ADORGLOH"


def create_pdf(text):
    try:
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Helvetica", size=12) # Helvetica est plus standard que Arial
        
        # Nettoyage pour éviter les erreurs d'encodage avec fpdf
        clean_text = text.encode('latin-1', 'ignore').decode('latin-1')
        
        pdf.multi_cell(0, 10, txt=clean_text)
        
        # .output() renvoie un bytearray, on le convertit en bytes
        return bytes(pdf.output()) 
    except Exception as e:
        logger.error(f"PDF Generation Error: {e}")
        return None

# 3. EXTRACTION LOGIC
def extract_text_from_url(url):
    try:
        res = requests.get(url, timeout=10)
        res.raise_for_status()
        soup = BeautifulSoup(res.text, 'html.parser')
        text = " ".join([p.get_text() for p in soup.find_all('p')])
        return text if text.strip() else None
    except Exception as e:
        logger.error(f"URL Error: {e}")
        return None

def extract_text_from_pdf(file):
    try:
        reader = PyPDF2.PdfReader(file)
        return " ".join([page.extract_text() for page in reader.pages])
    except Exception as e:
        logger.error(f"PDF Upload Error: {e}")
        return None


def get_ai_summary(text):
    try:
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            logger.error("API Key is missing!")
            return "Error: GOOGLE_API_KEY not found in environment."

        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-3-flash-preview')
        
        # On réduit la taille du texte pour être sûr de ne pas saturer l'API
        clean_input = text[:15000] 
        
        prompt = f"You are {ASSISTANT_NAME}. Summarize this in English:\n\n{clean_input}"
        
        response = model.generate_content(prompt)
        
        # Vérification si la réponse contient du texte
        if response.text:
            return response.text
        else:
            return "Gemini returned an empty response."

    except Exception as e:
        logger.error(f"AI Error: {str(e)}")
        # On affiche l'erreur réelle pour débugger
        return f"AI Error details: {str(e)}"
# --- UI DESIGN ---
st.set_page_config(page_title=f"{ASSISTANT_NAME} AI", page_icon="⚡", layout="wide")

# Custom CSS for a "prettier" look
st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .stButton>button { width: 100%; border-radius: 5px; height: 3em; background-color: #FF4B4B; color: white; }
    </style>
    """, unsafe_allow_html=True)

st.title(f"🤖 {ASSISTANT_NAME} Smart Assistant")
st.info(f"Hi, I'm **{ASSISTANT_NAME}** a successful entrepreneur. I can summarize any article or PDF for you in seconds.")

col1, col2 = st.columns([1, 1], gap="large")

with col1:
    st.subheader("📥 Input Source")
    option = st.selectbox("How would you like to provide the content?", ["URL Link 🔗", "Upload PDF 📄"])
    
    input_data = ""
    if option == "URL Link 🔗":
        url = st.text_input("Paste the article URL here:")
        if url: input_data = extract_text_from_url(url)
    else:
        file = st.file_uploader("Upload your PDF file:", type="pdf")
        if file: input_data = extract_text_from_pdf(file)

with col2:
    st.subheader("📝 Summary Output")
    if st.button("Generate Summary"):
        if input_data:
            with st.spinner(f"{ASSISTANT_NAME} is thinking..."):
                summary = get_ai_summary(input_data)
                st.markdown(f"**{ASSISTANT_NAME}'s Analysis:**")
                st.write(summary)
                
                # Download Button
                pdf_bytes = create_pdf(summary)
                st.download_button(
                    label="📥 Download Summary as PDF",
                    data=pdf_bytes,
                    file_name=f"summary_{ASSISTANT_NAME}.pdf",
                    mime="application/pdf"
                )
                logger.info(f"Summary generated successfully for {option}")
        else:
            st.error("Please provide a valid source first.")