import streamlit as st
import google.generativeai as genai
from PIL import Image
from PyPDF2 import PdfReader
import io
import pandas as pd

# 1. Sahifa sozlamalari
st.set_page_config(page_title="Mahalla Ijro | Zangiota", page_icon="🏛", layout="wide")

# --- LOGIN TIZIMI ---
def check_password():
    if "password_correct" not in st.session_state:
        st.session_state["password_correct"] = False

    if st.session_state["password_correct"]:
        return True

    # Kirish oynasi dizayni (To'liq lotincha)
    st.markdown("<h1 style='text-align: center; color: #385723;'>🏛 Mahalla Ijro Tizimi</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center;'>Tizimga kirish uchun login va parolni kiriting</p>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        username = st.text_input("Login")
        password = st.text_input("Parol", type="password")
        if st.button("Kirish"):
            creds = st.secrets.get("credentials", {})
            if username in creds and str(creds[username]) == password:
                st.session_state["password_correct"] = True
                st.rerun()
            else:
                st.error("❌ Login yoki parol noto'g'ri!")
    return False

if not check_password():
    st.stop()

# --- ASOSIY DASTUR ---
# API Sozlamasi (Xatoga chidamli)
if "GEMINI_API_KEY" in st.secrets:
    try:
        genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
        try:
            model = genai.GenerativeModel('gemini-1.5-flash')
            model.generate_content("test") 
        except:
            model = genai.GenerativeModel('models/gemini-1.5-flash')
    except Exception as e:
        st.error(f"API ulanishda xato: {e}")

# Sidebar Menyu (Lotincha)
with st.sidebar:
    st.image("https://upload.wikimedia.org/wikipedia/commons/7/77/Emblem_of_Uzbekistan.png", width=80)
    st.markdown("### 📋 MENYU")
    menu = st.radio("", ["Javob xati yozish", "Muammolar tahlili"], label_visibility="collapsed")
    st.markdown("---")
    if st.button("Chiqish"):
        st.session_state["password_correct"] = False
        st.rerun()

# Mas'ul rahbarlar ro'yxati (Lotincha)
positions = [
    "1. Mahalla uyushmasi tuman bo'limi boshlig'i",
    "2. Tuman Ichki ishlar bo'limi boshlig'i",
    "3. 'Inson' ijtimoiy xizmatlar markazi direktori",
    "4. Yoshlar ishlari agentligi tuman bo'limi boshlig'i",
    "5. Soliq qo'mitasi tuman bo'limi boshlig'i",
    "6. Oila va xotin-qizlar qo'mitasi tuman bo'limi boshlig'i",
    "7. Mahallabay ishlash agentligi boshlig'i"
]
