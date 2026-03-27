import streamlit as st
import google.generativeai as genai
from PIL import Image
from PyPDF2 import PdfReader
import io
import pandas as pd

# 1. Sahifa sozlamalari
st.set_page_config(page_title="Mahalla Ijro | Zangiota", page_icon="🏛", layout="wide")

# Maxsus dizayn
st.markdown("""
    <style>
    .stApp { background-color: #fdfdfd; }
    [data-testid="stSidebar"] { background-color: #e2efda; }
    .stButton>button { width: 100%; border-radius: 5px; background-color: #70ad47; color: white; border: none; font-weight: bold; }
    h1, h2, h3 { color: #385723; }
    </style>
    """, unsafe_allow_html=True)

# 2. API Sozlamasi (Xatoni avtomatik tuzatuvchi variant)
if "GEMINI_API_KEY" in st.secrets:
    try:
        genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
        
        # Qaysi model nomi ishlashini tekshiramiz
        try:
            model = genai.GenerativeModel('gemini-1.5-flash')
            # Test so'rovi (model bormi yoki yo'qligini tekshirish uchun)
            model.generate_content("test") 
        except:
            model = genai.GenerativeModel('models/gemini-1.5-flash')
            
    except Exception as e:
        st.error(f"API ulanishda xato: {e}")
else:
    st.error("Secrets bo'limida API kalit topilmadi!")

# 3. Sidebar Menyu
with st.sidebar:
    st.image("https://upload.wikimedia.org/wikipedia/commons/7/77/Emblem_of_Uzbekistan.png", width=80)
    st.markdown("### 📋 МЕНЮ")
    menu = st.radio("", ["Javob xati yozish", "Muammolar tahlili (Hisobot)"], label_visibility="collapsed")

# 4. Ma'lumotlar
positions = [
    "1. Mahalla uyushmasi tuman bo'limi boshlig'i",
    "2. Tuman Ichki ishlar bo'limi boshlig'i",
    "3. 'Inson' ijtimoiy xizmatlar markazi direktori",
    "4. Yoshlar ishlari agentligi tuman bo'limi boshlig'i",
    "5. Soliq qo'mitasi tuman bo'limi boshlig'i",
    "6. Oila va xotin-qizlar qo'mitasi tuman bo'limi boshlig'i",
    "7. Mahallabay ishlash agentligi boshlig'i"
]

# --- MENYU: JAVOB XATI YOZISH ---
if menu == "Javob xati yozish":
    st.title("🏛 МАХАЛЛА ИЖРО Zangiota tumani")
    st.write("📄 Hujjat turini tanlang va asosiy faylni yuklang.")
    
    hujjat_turi = st.radio("", ["Javob xati", "Ma'lumotnoma", "Yig'ilish bayoni", "Dalolatnoma", "Bildirishnoma"], horizontal=True)
    murojaat = st.file_uploader("📥 Asosiy faylni yuklang (PDF yoki Rasm):", type=['png', 'jpg', 'jpeg', 'pdf'])

    if murojaat:
        st.markdown("---")
        col1, col2 = st.columns(2)
        with col1:
            rahbar = st.selectbox("👤 Mas'ul rahbarn tanlang:", positions)
            ilova = st.file_uploader("📎 Ilova (ixtiyoriy):", type=['png', 'jpg', 'jpeg', 'pdf'])
        with col2:
            izoh = st.text_area("✍️ Qo'shimcha ko'rsatma:", placeholder="Masalan: Arizani qanoatlantirish haqida...", height=120)

        if st.button("🚀 HUJJATNI TAYYORLASH"):
            with st.spinner("⏳ AI tahlil qilmoqda..."):
                try:
                    prompt = f"Siz {rahbar}siz. Yuklangan hujjat asosida professional '{hujjat_turi}' tayyorlang. Lotin alifbosida yozing. MFY nomini avtomatik qo'shmang."
                    content = [prompt]
                    if murojaat.type == "application/pdf":
                        reader = PdfReader(io.BytesIO(murojaat.read()))
                        content.append("Hujjat matni: " + "".join([p.extract_text() for p in reader.pages]))
                    else:
                        content.append(Image.open(murojaat))
                    if izoh: content.append(f"Izoh: {izoh}")
                    
                    res = model.generate_content(content)
                    st.success("✅ Tayyorlandi!")
                    st.info(res.text)
                except Exception as e:
                    st.error(f"Xatolik yuz berdi: {e}")

# --- MENYU: HISOBOT ---
elif menu == "Muammolar tahlili (Hisobot)":
    st.title("📊 Murojaatlardagi muammolar tahlili")
    stats_data = {
        "Muammo yo'nalishi": ["Gaz", "Elektr", "Suv", "Yo'l", "Yordam", "Bandlik", "Boshqa"],
        "Kelib tushgan": [45, 38, 22, 56, 89, 41, 15],
        "Hal etilgan": [30, 25, 15, 20, 75, 30, 10]
    }
    df = pd.DataFrame(stats_data)
    st.table(df)
    st.bar_chart(df.set_index("Muammo yo'nalishi")["Kelib tushgan"])
