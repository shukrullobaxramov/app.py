# -*- coding: utf-8 -*-
import streamlit as st
import google.generativeai as genai
from PIL import Image
from PyPDF2 import PdfReader
import io
import pandas as pd

# 1. Sahifa sozlamalari
st.set_page_config(page_title="Mahijro AI | Zangiota 60 MFY", page_icon="🏛", layout="wide")

# Dizayn (CSS)
st.markdown("""
    <style>
    .main { background-color: #f0f2f6; }
    .stButton>button { width: 100%; border-radius: 8px; height: 3em; background-color: #004a99; color: white; font-weight: bold; }
    .sidebar .sidebar-content { background-image: linear-gradient(#2e7d32, #1b5e20); color: white; }
    </style>
    """, unsafe_allow_html=True)

# 2. Login tizimi
if "logged_in" not in st.session_state:
    st.markdown("<h2 style='text-align: center;'>🏛 Mahijro AI: Zangiota tumani tizimiga kirish</h2>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 1.2, 1])
    with col2:
        u = st.text_input("Login:")
        p = st.text_input("Parol:", type="password")
        if st.button("Tizimga kirish"):
            if u == "admin" and p == "zangiota2026":
                st.session_state["logged_in"] = True
                st.rerun()
            else:
                st.error("Login yoki parol xato!")
    st.stop()

# 3. API Sozlamalari
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    model = genai.GenerativeModel(model_name="models/gemini-1.5-flash")
else:
    st.error("API kalit topilmadi! Streamlit Secrets-ni tekshiring.")
    st.stop()

# 4. Sidebar - MFYlar ro'yxati va Hisobotlar
st.sidebar.image("https://upload.wikimedia.org/wikipedia/commons/thumb/7/70/Coat_of_arms_of_Uzbekistan.svg/1200px-Coat_of_arms_of_Uzbekistan.svg.png", width=100)
st.sidebar.title("Zangiota tumani")
st.sidebar.subheader("60 ta MFY monitoringi")

# MFYlar ro'yxati (Asosiylari, qolganlarini ham qo'shish mumkin)
mfy_list = [
    "Alimbuva", "Sortepa", "Erkin", "O'rtaovul", "Tiklanish", "Mustaqillik", 
    "Bog'zor", "G'uliston", "Ittifoq", "Zangiota", "Navro'z", "Nazarbek"
] # Bu yerga barcha 60 ta MFY nomini kiritish mumkin

selected_mfy = st.sidebar.selectbox("Mahallani tanlang:", mfy_list)
menu = st.sidebar.radio("Bo'limni tanlang:", ["Javob xati yozish", "MFY Hisobot shakllari", "Tizim statistikasi"])

# --- BO'LIM 1: JAVOB XATI YOZISH ---
if menu == "Javob xati yozish":
    st.title(f"🏛 {selected_mfy} MFY: Javob xati generatori")
    st.info("Murojaat va o'rganish ma'lumotlarini yuklang.")

    col1, col2 = st.columns(2)
    with col1:
        murojaat_file = st.file_uploader("Fuqaro arizasi (PDF/Rasm)", type=['png', 'jpg', 'pdf'])
    with col2:
        organish_matni = st.text_area("O'rganish natijasi (Izoh):", placeholder="Masalan: Joyiga borib ko'rildi...", height=100)

    if st.button("🚀 Javob xati loyihasini tayyorlash"):
        if murojaat_file:
            with st.spinner("AI tahlil qilmoqda..."):
                try:
                    prompt = f"""Siz Zangiota tumani {selected_mfy} MFY mutaxassisiz. 
                    Murojaat va o'rganish ma'lumotlarini tahlil qilib, fuqaroga rasmiy javob yozing.
                    1. Matn FAQAT LOTIN alifbosida bo'lsin.
                    2. Rasmiy blanka talablariga mos bo'lsin.
                    3. MFY nomi: {selected_mfy} deb ko'rsatilsin.
                    """
                    input_data = [prompt]
                    if murojaat_file.type == "application/pdf":
                        reader = PdfReader(io.BytesIO(murojaat_file.read()))
                        input_data.append("".join([p.extract_text() for p in reader.pages]))
                    else:
                        input_data.append(Image.open(murojaat_file))
                    if organish_matni: input_data.append(f"IZOH: {organish_matni}")

                    res = model.generate_content(input_data)
                    st.success(f"✅ {selected_mfy} MFY uchun javob tayyor!")
                    st.write(res.text)
                except Exception as e:
                    st.error(f"Xatolik: {e}")
        else:
            st.warning("Arizani yuklang.")

# --- BO'LIM 2: MFY HISOBOT SHAKLLARI ---
elif menu == "MFY Hisobot shakllari":
    st.title(f"📊 {selected_mfy} MFY bo'yicha hisobot shakllari")
    
    st.write("Ushbu bo'limda mahalladagi kirish-chiqish xatlari va protokollar jamlanadi.")
    
    # Namuna sifatida jadval shakli
    data = {
        "Hujjat turi": ["Kirish (Ariza)", "Chiqish (Javob)", "Bayonnoma", "Dalolatnoma"],
        "Soni": [12, 10, 2, 5],
        "Holati": ["Bajarilgan", "Jarayonda", "Tasdiqlangan", "Yopilgan"]
    }
    df = pd.DataFrame(data)
    st.table(df)
    
    st.download_button("Excel hisobotni yuklab olish (XLSX)", data="Sample data", file_name=f"{selected_mfy}_hisobot.xlsx")

# --- BO'LIM 3: TIZIM STATISTIKASI ---
elif menu == "Tizim statistikasi":
    st.title("📈 Zangiota tumani: Umumiy tahlil")
    col1, col2, col3 = st.columns(3)
    col1.metric("Jami MFYlar", "60 ta")
    col2.metric("Bugungi murojaatlar", "45 ta")
    col3.metric("Bajarilish ko'rsatkichi", "94%")
    
    st.bar_chart({"Murojaat": [15, 30, 45, 20], "Javob": [10, 25, 40, 18]})

st.sidebar.markdown("---")
st.sidebar.caption("© 2026 Mahijro AI - Zangiota tumani Mahalla uyushmasi")
