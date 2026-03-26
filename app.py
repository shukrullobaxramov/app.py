# -*- coding: utf-8 -*-
import streamlit as st
import google.generativeai as genai
from PIL import Image
from PyPDF2 import PdfReader
import io

# 1. Sahifa va Dizayn
st.set_page_config(page_title="Mahijro AI | Markaziy Boshqaruv", page_icon="🏛", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #f4f7f9; }
    .stButton>button { width: 100%; border-radius: 6px; height: 3.5em; background-color: #0d47a1; color: white; font-weight: bold; }
    .stSelectbox label { font-weight: bold; color: #0d47a1; }
    </style>
    """, unsafe_allow_html=True)

# 2. Rahbarlik lavozimlari (7 ta asosiy bo'lim)
positions = [
    "1. Mahalla uyushmasi tuman bo'limi boshlig'i",
    "2. Tuman Ichki ishlar bo'limi boshlig'i",
    "3. 'Inson' ijtimoiy xizmatlar markazi direktori",
    "4. Yoshlar ishlari agentligi tuman bo'limi boshlig'i",
    "5. Soliq qo'mitasi tuman bo'limi boshlig'i",
    "6. Oila va xotin-qizlar qo'mitasi tuman bo'limi boshlig'i",
    "7. Mahallabay ishlash va tadbirkorlikni rivojlantirish agentligi boshlig'i"
]

# 60 ta MFY ro'yxati (Siz bergan tartibda)
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

# 3. Login mantiqi
if "logged_in" not in st.session_state:
    st.markdown("<h1 style='text-align: center; color: #0d47a1;'>🏛 MAHIJRO AI</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center;'>Zangiota tumani mas'ul rahbarlari uchun qaror qabul qilish tizimi</p>", unsafe_allow_html=True)
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

# 4. AI Sozlamasi
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
model = genai.GenerativeModel('gemini-1.5-flash')

# 5. Sidebar
st.sidebar.image("https://upload.wikimedia.org/wikipedia/commons/thumb/7/70/Coat_of_arms_of_Uzbekistan.svg/1200px-Coat_of_arms_of_Uzbekistan.svg.png", width=70)
st.sidebar.title("Zangiota tumani")
st.sidebar.info("Markaziy boshqaruv va tahlil tizimi")

# 6. Asosiy Interfeys
st.title("🏛 Rasmiy hujjatlar generatori")
st.markdown("---")

col_a, col_b = st.columns(2)

with col_a:
    selected_pos = st.selectbox("Mas'ul rahbar (Lavozim):", positions)
    selected_mfy = st.selectbox("Tegishli mahalla:", mfy_list)
    murojaat_f = st.file_uploader("Fuqaro murojaati (PDF/Rasm):", type=['png', 'jpg', 'pdf'], key="m1")

with col_b:
    dalolatnoma_f = st.file_uploader("O'rganish dalolatnomasi (Ixtiyoriy):", type=['png', 'jpg', 'pdf'], key="d1")
    ko_rsatma = st.text_area("Rahbar ko'rsatmasi yoki qo'shimcha ma'lumot:", 
                            placeholder="Masalan: Qonun doirasida ijobiy hal etilsin yoki tushuntirish berilsin...", height=110)

if st.button("🚀 RASMIY JAVOBNI SHAKLLANTIRISH"):
    if murojaat_f:
        with st.spinner("AI tahlil qilmoqda..."):
            try:
                # Promptni lavozimga qarab moslashtirish
                prompt = f"""Siz {selected_pos}siz. 
                Sizga {selected_mfy} mahallasidan murojaat kelgan. 
                Vazifangiz: O'z sohangizdan kelib chiqib (masalan, agar Soliq bo'lsa - soliq qonunchiligi, 
                agar 'Inson' markazi bo'lsa - ijtimoiy himoya qoidalari asosida) fuqaroga 
                rasmiy, lotin alifbosida, savodli javob xati loyihasini tayyorlash.
                Hujjatda lavozimingizni aniq ko'rsating. Til: O'zbek (lotin).
                """
                
                content = [prompt]
                
                # Fayllarni o'qish
                if murojaat_f.type == "application/pdf":
                    content.append("MUROJAAT: " + "".join([p.extract_text() for p in PdfReader(io.BytesIO(murojaat_f.read())).pages]))
                else:
                    content.append(Image.open(murojaat_f))
                
                if dalolatnoma_f:
                    if dalolatnoma_f.type == "application/pdf":
                        content.append("DALOLATNOMA: " + "".join([p.extract_text() for p in PdfReader(io.BytesIO(dalolatnoma_f.read())).pages]))
                    else:
                        content.append(Image.open(dalolatnoma_f))
                
                if ko_rsatma:
                    content.append(f"RAHBAR KO'RSATMASI: {ko_rsatma}")

                response = model.generate_content(content)
                st.success(f"✅ {selected_pos} uchun javob loyihasi tayyor!")
                st.markdown("---")
                st.write(response.text)
                
            except Exception as e:
                st.error(f"Xatolik yuz berdi: {str(e)}")
    else:
        st.warning("Iltimos, avval murojaat faylini yuklang.")

st.sidebar.markdown("---")
st.sidebar.write("**Tizim nazorati:** 2026-yil, Zangiota.")
