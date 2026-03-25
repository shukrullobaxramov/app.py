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
    </style>
    """, unsafe_allow_html=True)

# 2. Zangiota tumanidagi aynan siz bergan 60 ta MFY ro'yxati
mfy_list = [
    "Abdujalilbob", "Alimbuva", "Amir Temur", "Asil", "Axilobod", "Ahmad Yassaviy",
    "Baliqchi", "Bog'zor", "Bog'ishamol", "Bodomzor", "Bo'ston", "Gulbog'",
    "Daligazar", "Dehqonobod", "Zarafshon", "Ilg'or", "Istiqlol", "Istiqlolning 5-yilligi",
    "Katta chinor", "Keng kechik", "Qahramon", "Quyoshli", "Qurilish", "M.M.Xorazmiy",
    "Madaniyat", "Mevazor", "Navbahor", "Navqiron", "Nazarbek", "Nayman",
    "Namuna", "Nurafshon", "Nurobod", "Obod", "Obod to'qimachi", "Obod turmush",
    "Olmazor", "Ramadon", "Saxovat", "Sortepa", "Tariq-teshar", "Tarnov",
    "Tokzor", "To'qimachi", "Turkiston", "Turopobod", "O'ratepa", "O'rikzor",
    "O'rta", "O'rtaovul", "Fayz", "Farobiy", "Harakat", "Xo'jamozor",
    "Chinor", "Shodlik", "Erkin", "Eski qala", "Eshonguzar", "Yangi bo'zsuv"
]

# 3. Login tizimi
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

# 4. API Sozlamalari
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    model = genai.GenerativeModel(model_name="models/gemini-1.5-flash")
else:
    st.error("API kalit topilmadi!")
    st.stop()

# 5. Sidebar - Navigatsiya
st.sidebar.title("Zangiota tumani")
st.sidebar.subheader("Mahalla boshqaruvi")

selected_mfy = st.sidebar.selectbox("Mahallani tanlang (60 ta):", mfy_list)
menu = st.sidebar.radio("Bo'limni tanlang:", ["Javob xati yozish", "MFY Hisobot shakllari"])

# --- BO'LIM 1: JAVOB XATI YOZISH ---
if menu == "Javob xati yozish":
    st.title(f"🏛 {selected_mfy} MFY: Javob xati generatori")
    st.markdown("---")

    col_left, col_right = st.columns(2)
    
    with col_left:
        st.subheader("1. Murojaatni yuklang")
        murojaat_file = st.file_uploader("Fuqaro arizasi (PDF yoki Rasm)", type=['png', 'jpg', 'jpeg', 'pdf'], key="m_file")

    with col_right:
        st.subheader("2. O'rganish ma'lumotlari")
        # DALOLATNOMA QISMI (Ixtiyoriy)
        organish_file = st.file_uploader("O'rganish dalolatnomasi (Ixtiyoriy)", type=['png', 'jpg', 'jpeg', 'pdf'], key="o_file")
        organish_matni = st.text_area("Qo'shimcha izoh yoki joyidagi holat (Ixtiyoriy):", 
                                     placeholder="Masalan: Murojaat joyiga borib o'rganildi...", height=110)

    if st.button("🚀 Javob xati loyihasini shakllantirish"):
        if murojaat_file:
            with st.spinner("Hujjatlar tahlil qilinmoqda..."):
                try:
                    prompt = f"""Siz Zangiota tumani {selected_mfy} MFY mutaxassisiz. 
                    Yuklangan murojaat va o'rganish ma'lumotlarini tahlil qilib, rasmiy javob yozing.
                    - Matn FAQAT LOTIN alifbosida bo'lsin.
                    - MFY nomi: {selected_mfy} deb ko'rsatilsin.
                    - Rasmiy ish yuritish standartlariga amal qiling.
                    """
                    input_data = [prompt]
                    
                    if murojaat_file.type == "application/pdf":
                        pdf_reader = PdfReader(io.BytesIO(murojaat_file.read()))
                        input_data.append("".join([page.extract_text() for page in pdf_reader.pages]))
                    else:
                        input_data.append(Image.open(muro_file := murojaat_file))
                    
                    if organish_file:
                        if organish_file.type == "application/pdf":
                            pdf_reader_o = PdfReader(io.BytesIO(organish_file.read()))
                            input_data.append("".join([page.extract_text() for page in pdf_reader_o.pages]))
                        else:
                            input_data.append(Image.open(organish_file))
                            
                    if organish_matni:
                        input_data.append(f"IZOH: {organish_matni}")

                    response = model.generate_content(input_data)
                    st.success(f"✅ {selected_mfy} MFY uchun javob loyihasi tayyor!")
                    st.markdown("---")
                    st.write(response.text)
                except Exception as e:
                    st.error(f"Xatolik: {str(e)}")
        else:
            st.warning("Iltimos, avval murojaatni yuklang.")

# --- BO'LIM 2: MFY HISOBOT SHAKLLARI ---
elif menu == "MFY Hisobot shakllari":
    st.title(f"📊 {selected_mfy} MFY: Hisobot va Tahlil")
    
    report_data = {
        "Ko'rsatkich": ["Kelib tushgan arizalar", "Tayyorlangan javoblar", "O'rganish bosqichida", "Rad etilgan"],
        "Soni": [24, 21, 2, 1]
    }
    st.table(pd.DataFrame(report_data))
    
    st.info(f"Hozirda {selected_mfy} MFY bo'yicha tizimda 24 ta hujjat qayd etilgan.")

st.sidebar.markdown("---")
st.sidebar.caption("© 2026 Mahijro AI - Zangiota tumani")
