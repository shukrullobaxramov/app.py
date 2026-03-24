# -*- coding: utf-8 -*-
import streamlit as st
import google.generativeai as genai
from PIL import Image
from PyPDF2 import PdfReader
import pandas as pd

# Sahifa sozlamalari
st.set_page_config(page_title="Mahijro AI", page_icon="🏛", layout="wide")

# API Sozlash (404 xatosini yo'qotish uchun)
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    model = genai.GenerativeModel('gemini-1.5-flash')
else:
    st.error("API kalit topilmadi!")
    st.stop()

# MFY ro'yxati (Jami 59 ta)
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
tab1, tab2 = st.tabs(["✍️ Murojaat tahlili", "📊 MFY hisoboti"])

with tab1:
    st.subheader("Murojaatga javob tayyorlash")
    uploaded_file = st.file_uploader("Faylni yuklang (PDF yoki Rasm)", type=['png', 'jpg', 'jpeg', 'pdf'])
    selected_mfy = st.selectbox("Mahallani tanlang:", malla_nomlari)
    
    if st.button("📝 Javob xati loyihasini yaratish"):
        if uploaded_file:
            with st.spinner("AI tahlil qilmoqda..."):
                try:
                    content = [f"Siz {selected_mfy} MFY raisisiz. Rasmiy javob xati loyihasini yozing."]
                    if uploaded_file.type == "application/pdf":
                        pdf_reader = PdfReader(uploaded_file)
                        text = "".join([page.extract_text() for page in pdf_reader.pages])
                        content.append(f"Hujjat matni: {text[:4000]}")
                    else:
                        content.append(Image.open(uploaded_file))
                    
                    response = model.generate_content(content)
                    st.write(response.text)
                except Exception as e:
                    st.error(f"Xatolik: {e}")

with tab2:
    st.subheader("Monitoring")
    # ValueError'ni oldini olish (len yordamida avtomatik tenglashtirish)
    df = pd.DataFrame({
        "№": range(1, len(malla_nomlari) + 1),
        "MFY nomi": malla_nomlari,
        "Holat": ["Yangi"] * len(malla_nomlari)
    })
    st.dataframe(df, use_container_width=True, hide_index=True)
