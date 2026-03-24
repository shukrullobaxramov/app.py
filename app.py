# -*- coding: utf-8 -*-
import streamlit as st
import google.generativeai as genai
from PIL import Image
from PyPDF2 import PdfReader
import pandas as pd

# Sahifa sozlamalari
st.set_page_config(page_title="Mahijro AI", page_icon="🏛", layout="wide")

# Login tizimi
if "logged_in" not in st.session_state:
    st.markdown("<h2 style='text-align: center;'>🏛 Mahijro AI: Kirish</h2>", unsafe_allow_html=True)
    u = st.text_input("Login:")
    p = st.text_input("Parol:", type="password")
    if st.button("Kirish", use_container_width=True):
        if u == "admin" and p == "zangiota2026":
            st.session_state["logged_in"] = True
            st.rerun()
        else: st.error("Xato!")
    st.stop()

# API sozlash
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
else:
    st.error("API kalit topilmadi!")
    st.stop()

# 404 xatosini oldini olish uchun modelni to'g'ri chaqirish
model = genai.GenerativeModel('gemini-1.5-flash')

# Alifbo bo'yicha mahallalar
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

st.title("🏛 Mahijro AI: Ishchi paneli")
uploaded_file = st.file_uploader("Murojaatni yuklang (PDF yoki Rasm)", type=['png', 'jpg', 'jpeg', 'pdf'])
selected_mfy = st.selectbox("Mahallani tanlang:", malla_nomlari)
murojaat_izoh = st.text_area("Rezolyutsiya:")

if st.button("📝 Javob xati loyihasini yaratish"):
    if uploaded_file or murojaat_izoh:
        with st.spinner("Tahlil qilinmoqda..."):
            try:
                content = [f"Siz Zangiota tumani {selected_mfy} MFY raisisiz. Rasmiy javob yozing:"]
                if murojaat_izoh: content.append(murojaat_izoh)
                
                if uploaded_file:
                    if uploaded_file.type == "application/pdf":
                        pdf = PdfReader(uploaded_file)
                        matn = ""
                        for page in pdf.pages:
                            matn += page.extract_text()
                        content.append(f"PDF matni: {matn[:5000]}") # PDF matnini qo'shish
                    else:
                        content.append(Image.open(uploaded_file))

                response = model.generate_content(content)
                st.success("Javob тайёр:")
                st.write(response.text)
            except Exception as e:
                if "429" in str(e): st.error("Limit tugadi. 1 daqiqa kuting.")
                else: st.error(f"Xatolik: {e}")
