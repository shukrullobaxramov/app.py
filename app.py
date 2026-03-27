# -*- coding: utf-8 -*-
import streamlit as st
import google.generativeai as genai
from PIL import Image
from PyPDF2 import PdfReader
import io

# 1. Sahifa sozlamalari
st.set_page_config(page_title="Mahijro AI | Markaziy Boshqaruv", page_icon="🏛", layout="wide")

# 2. Login tizimi
if "logged_in" not in st.session_state:
    st.markdown("<h1 style='text-align: center; color: #0d47a1;'>🏛 MAHIJRO AI</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center;'>Zangiota tumani mas'ul rahbarlari uchun tizim</p>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        u = st.text_input("Login:")
        p = st.text_input("Parol:", type="password")
        if st.button("Tizimga kirish"):
            if u == "admin" and p == "zangiota2026":
                st.session_state["logged_in"] = True
                st.rerun()
            else:
                st.error("Kirish taqiqlandi!")
    st.stop()

# 3. API va Model Sozlamasi (XATOSIZ)
try:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    # Eng barqaror model nomi: gemini-1.5-flash (oxiri 'h' bilan)
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    st.error(f"API ulanishda xatolik: {e}")
    st.stop()

# 4. Ma'lumotlar: 7 ta Rahbar va 60 ta MFY
positions = [
    "1. Mahalla uyushmasi tuman bo'limi boshlig'i",
    "2. Tuman Ichki ishlar bo'limi boshlig'i",
    "3. 'Inson' ijtimoiy xizmatlar markazi direktori",
    "4. Yoshlar ishlari agentligi tuman bo'limi boshlig'i",
    "5. Soliq qo'mitasi tuman bo'limi boshlig'i",
    "6. Oila va xotin-qizlar qo'mitasi tuman bo'limi boshlig'i",
    "7. Mahallabay ishlash va tadbirkorlikni rivojlantirish agentligi boshlig'i"
]

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

# 5. Interfeys
st.sidebar.image("https://upload.wikimedia.org/wikipedia/commons/thumb/7/70/Coat_of_arms_of_Uzbekistan.svg/1200px-Coat_of_arms_of_Uzbekistan.svg.png", width=70)
st.sidebar.title("Zangiota tumani")
st.sidebar.write("Markaziy boshqaruv")

st.title("🏛 Rasmiy javob xati generatori")
st.markdown("---")

col1, col2 = st.columns(2)

with col1:
    rahbar = st.selectbox("Mas'ul rahbar (Lavozim):", positions)
    mfy = st.selectbox("Tegishli mahalla:", mfy_list)
    murojaat_file = st.file_uploader("Fuqaro murojaati (PDF yoki Rasm):", type=['png', 'jpg', 'jpeg', 'pdf'])

with col2:
    dalolatnoma_file = st.file_uploader("O'rganish dalolatnomasi (Ixtiyoriy):", type=['png', 'jpg', 'jpeg', 'pdf'])
    izoh = st.text_area("Qo'shimcha ko'rsatma:", placeholder="Masalan: Arizani qanoatlantirish haqida...", height=110)

# 6. Generatsiya
if st.button("🚀 JAVOBNI TAYYORLASH"):
    if murojaat_file:
        with st.spinner("Hujjatlar tahlil qilinmoqda..."):
            try:
                # Prompt mantiqi
                prompt = f"""Siz {rahbar}siz. {mfy} mahallasidan kelgan murojaatni o'rganib chiqib, 
                fuqaroga rasmiy javob xati yozing. Matn LOTIN alifbosida, rasmiy ish yuritish uslubida bo'lsin.
                Soha bo'yicha qonuniy asoslarni keltiring.
                """
                content = [prompt]
                
                # Murojaatni o'qish
                if murojaat_file.type == "application/pdf":
                    reader = PdfReader(io.BytesIO(murojaat_file.read()))
                    content.append("MUROJAAT: " + "".join([p.extract_text() for p in reader.pages]))
                else:
                    content.append(Image.open(murojaat_file))
                
                # Dalolatnomani o'qish
                if dalolatnoma_file:
                    if dalolatnoma_file.type == "application/pdf":
                        reader_d = PdfReader(io.BytesIO(dalolatnoma_file.read()))
                        content.append("DALOLATNOMA: " + "".join([p.extract_text() for p in reader_d.pages]))
                    else:
                        content.append(Image.open(dalolatnoma_file))
                
                if izoh:
                    content.append(f"QO'SHIMCHA IZOH: {izoh}")

                # AI javobi
                response = model.generate_content(content)
                st.success("✅ Rasmiy javob loyihasi tayyor!")
                st.markdown("---")
                st.write(response.text)
                
            except Exception as e:
                st.error(f"Xatolik yuz berdi: {e}")
    else:
        st.warning("Iltimos, murojaat faylini yuklang.")

st.sidebar.markdown("---")
st.sidebar.caption("© 2026 Mahijro AI - Zangiota")
