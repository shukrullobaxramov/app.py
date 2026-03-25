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
    st.error("API kalit topilmadi!")
    st.stop()

# 4. Sidebar - MFYlar ro'yxati
st.sidebar.title("Zangiota tumani")
st.sidebar.subheader("60 ta MFY monitoringi")

mfy_list = [
    "Alimbuva", "Sortepa", "Erkin", "O'rtaovul", "Tiklanish", "Mustaqillik", 
    "Bog'zor", "G'uliston", "Ittifoq", "Zangiota", "Navro'z", "Nazarbek"
] # 60 ta MFY nomini shu yerga qo'shish mumkin

selected_mfy = st.sidebar.selectbox("Mahallani tanlang:", mfy_list)
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
        # SIZ SO'RAGAN JOY:
        organish_file = st.file_uploader("O'rganish dalolatnomasi (Ixtiyoriy)", type=['png', 'jpg', 'jpeg', 'pdf'], key="o_file")
        organish_matni = st.text_area("Qo'shimcha izoh yoki joyidagi holat (Ixtiyoriy):", 
                                     placeholder="Masalan: Murojaat joyiga borib o'rganildi...", height=110)

    if st.button("🚀 Javob xati loyihasini shakllantirish"):
        if murojaat_file:
            with st.spinner("Hujjatlar tahlil qilinmoqda va javob yozilmoqda..."):
                try:
                    prompt = f"""Siz Zangiota tumani {selected_mfy} MFY mutaxassisiz. 
                    Yuklangan murojaat va o'rganish ma'lumotlarini tahlil qilib, rasmiy javob yozing.
                    1. Matn FAQAT LOTIN alifbosida, rasmiy ish yuritish uslubida bo'lsin.
                    2. MFY nomi: {selected_mfy} deb ko'rsatilsin.
                    """
                    input_data = [prompt]
                    
                    # Murojaatni o'qish
                    if murojaat_file.type == "application/pdf":
                        pdf_reader = PdfReader(io.BytesIO(murojaat_file.read()))
                        m_text = "".join([page.extract_text() for page in pdf_reader.pages])
                        input_data.append(f"MUROJAAT MATNI: {m_text}")
                    else:
                        input_data.append(Image.open(murojaat_file))
                    
                    # Dalolatnomani o'qish (Agar yuklangan bo'lsa)
                    if organish_file:
                        if organish_file.type == "application/pdf":
                            pdf_reader_o = PdfReader(io.BytesIO(organish_file.read()))
                            o_text = "".join([page.extract_text() for page in pdf_reader_o.pages])
                            input_data.append(f"DALOLATNOMA MATNI: {o_text}")
                        else:
                            input_data.append(Image.open(organish_file))
                            
                    if organish_matni:
                        input_data.append(f"QO'SHIMCHA IZOH: {organish_matni}")

                    response = model.generate_content(input_data)
                    st.success("✅ Javob xati loyihasi tayyor!")
                    st.markdown("---")
                    st.write(response.text)
                except Exception as e:
                    st.error(f"Xatolik: {str(e)}")
        else:
            st.warning("Iltimos, avval murojaat faylini yuklang.")

# --- BO'LIM 2: MFY HISOBOT SHAKLLARI ---
elif menu == "MFY Hisobot shakllari":
    st.title(f"📊 {selected_mfy} MFY: Kirish-chiqish hisoboti")
    data = {
        "MFY nomi": [selected_mfy],
        "Kelib tushgan": [45],
        "Javob berilgan": [42],
        "Muddati o'tgan": [0],
        "Bajarilish %": ["93%"]
    }
    st.table(pd.DataFrame(data))
    st.info("Bu bo'limda keyinchalik 60 ta MFYning umumiy jadvali shakllanadi.")

st.sidebar.markdown("---")
st.sidebar.caption("© 2026 Mahijro AI - Zangiota tumani")
