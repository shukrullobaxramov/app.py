# -*- coding: utf-8 -*-
import streamlit as st
import google.generativeai as genai
from PIL import Image
from PyPDF2 import PdfReader
import pandas as pd

# 1. Sahifa sozlamalari
st.set_page_config(page_title="Mahijro AI", page_icon="🏛", layout="wide")

# 2. Login tizimi
if "logged_in" not in st.session_state:
    st.markdown("<h2 style='text-align: center;'>🏛 Mahijro AI: Tizimga kirish</h2>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        u = st.text_input("Login:")
        p = st.text_input("Parol:", type="password")
        if st.button("Kirish", use_container_width=True):
            if u == "admin" and p == "zangiota2026":
                st.session_state["logged_in"] = True
                st.rerun()
            else:
                st.error("Login yoki parol xato!")
    st.stop()

# 3. API Sozlash (404 xatosini yo'qotish uchun TUZATILGAN)
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    # MUHIM: v1beta ishlatilmaydi, bu ulanish xatosini to'g'irlaydi
    model = genai.GenerativeModel('gemini-1.5-flash')
else:
    st.error("API kalit topilmadi!")
    st.stop()

# 4. Mahallalar ro'yxati (Jami 59 ta)
malla_nomlari = [
    "Abdujalilbob", "Ahmad Yassaviy", "Alimbuva", "Amir Temur", "Asil", "Axilobod", 
    "Baliqchi", "Bodomzor", "Bog'ishamol", "Bog'zor", "Bo'ston", "Chinor", 
    "Dalgazar", "Dexkonobod", "Erkin", "Eshonguzar", "Eski qala", "Farobiy", 
    "Fayz", "Gulbog'", "Harakat", "Ilg'or", "Istiqlol", "Istiqlolning 5-yilligi", 
    "Katta chinor", "Keng kechik", "M.M.Xorazmiy", "Madaniyat", "Mevazor", 
    "Namuna", "Navbahor", "Navqiron", "Nayman", "Nazarbek", "Nurafshon", 
    "Nurobod", "Obod", "Obod to'qimachi", "Obod turmush", "Olmazor", "O'ratepa", 
    "O'rikzor", "O'rta", "O'rtaovul", "Qahramon", "Qurilish", "Quyoshli", 
    "Ramadon", "Saxovat", "Shodlik", "Sortecha", "Tariq-teshar", "Tarnov", 
    "Tokzor", "To'qimachi", "Turopobod", "Turkiston", "Xo'jamazor", "Yangi bo'suz"
]

st.title("🏛 Mahijro AI: Zangiota tumani")

tab1, tab2 = st.tabs(["✍️ Murojaat tahlili", "📊 MFY hisoboti"])

# ================= TAB 1: MUROJAATLAR =================
with tab1:
    st.subheader("Murojaatga javob tayyorlash")
    colA, colB = st.columns([1, 1])
    with colA:
        uploaded_file = st.file_uploader("Murojaatni yuklang (PDF yoki Rasm)", type=['png', 'jpg', 'jpeg', 'pdf'])
        selected_mfy = st.selectbox("Mas'ul mahallani tanlang:", malla_nomlari)
    with colB:
        muro_izoh = st.text_area("Rezolyutsiya yoki qo'shimcha topshiriq:", height=100)
    
    if st.button("📝 Javob xati loyihasini yaratish", use_container_width=True):
        if uploaded_file or muro_izoh:
            with st.spinner("AI tahlil qilmoqda..."):
                try:
                    prompt = f"Siz Zangiota tumani {selected_mfy} MFY raisisiz. Rasmiy va tartibli javob xati loyihasini tayyorlang."
                    content = [prompt]
                    if muro_izoh: content.append(f"Topshiriq: {muro_izoh}")
                    
                    if uploaded_file:
                        if uploaded_file.type == "application/pdf":
                            pdf_reader = PdfReader(uploaded_file)
                            text = "".join([page.extract_text() for page in pdf_reader.pages])
                            content.append(f"Hujjat matni: {text[:4000]}")
                        else:
                            content.append(Image.open(uploaded_file))

                    response = model.generate_content(content)
                    st.success("✅ Tayyorlangan javob:")
                    st.markdown(response.text)
                except Exception as e:
                    st.error(f"Xatolik yuz berdi: {e}")
        else:
            st.warning("Iltimos, fayl yuklang yoki matn kiriting.")

# ================= TAB 2: MONITORING =================
with tab2:
    st.subheader("Mahallalar monitoringi")
    # ValueError TUZATILGAN: len() yordamida avtomatik tenglashtirish
    df = pd.DataFrame({
        "№": range(1, len(malla_nomlari) + 1),
        "MFY nomi": malla_nomlari,
        "Holat": ["Yangi"] * len(malla_nomlari)
    })
    st.dataframe(df, use_container_width=True, hide_index=True)
