import streamlit as st
import google.generativeai as genai
from PIL import Image
from PyPDF2 import PdfReader
import io
import pandas as pd

# 1. Sahifa sozlamalari
st.set_page_config(page_title="Mahalla Ijro | Zangiota", page_icon="🏛", layout="wide")

# Maxsus CSS dizayn (Yashil va professional ranglar)
st.markdown("""
    <style>
    .stApp { background-color: #fdfdfd; }
    .sidebar .sidebar-content { background-color: #e2efda; }
    .stButton>button { width: 100%; border-radius: 5px; background-color: #70ad47; color: white; border: none; }
    h1, h2 { color: #385723; }
    .report-table { font-size: 14px; text-align: center; }
    </style>
    """, unsafe_allow_html=True)

# 2. API Sozlamasi
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    model = genai.GenerativeModel('gemini-1.5-flash')
else:
    st.error("API Key topilmadi!")

# 3. Sidebar Menyusi
with st.sidebar:
    st.markdown("## 📋 МЕНЮ")
    menu = st.radio("", ["Javob xati yozish", "Hisobot"], label_visibility="collapsed")
    
    st.markdown("---")
    positions = ["1. Mahalla uyushmasi boshlig'i", "2. IIB boshlig'i", "3. 'Inson' markazi direktori", "4. Yoshlar agentligi boshlig'i"]
    rahbar = st.selectbox("👤 Mas'ul rahbar:", positions)

# --- MENYU: JAVOB XATI YOZISH ---
if menu == "Javob xati yozish":
    st.title("🏛 МАХАЛЛА ИЖРО Zangiota tumani")
    st.subheader("Asosiy oyna")

    col1, col2 = st.columns([1.5, 1])

    with col1:
        st.write("📄 Hujjat turini tanlang va faylni yuklang.")
        hujjat_turi = st.radio("", ["Javob xati", "Ma'lumotnoma", "Yig'ilish bayoni", "Dalolatnoma", "Bildirishnoma"], horizontal=True)
        
        murojaat = st.file_uploader("📥 Asosiy faylni yuklang (Rasm/PDF):", type=['png', 'jpg', 'jpeg', 'pdf'])
        
        st.markdown("##### Далолатнома ёки малумотнома (ихтиёрий)")
        ilova = st.file_uploader("Ilovani yuklang:", type=['png', 'jpg', 'jpeg', 'pdf'], key="ilova")

    with col2:
        st.markdown("##### ✍️ Qo'shimcha ko'rsatma (Ixtiyoriy):")
        izoh = st.text_area("", placeholder="Masalan: Arizani rad etish sababini tushuntiring...", height=250)

    if st.button("🚀 ТАЙЁРЛАШ"):
        if murojaat:
            with st.spinner("⏳ AI tahlil qilmoqda..."):
                try:
                    content = [f"Siz {rahbar}siz. '{hujjat_turi}' tayyorlang. Lotin alifbosida yozing. MFY nomini avtomatik qo'shmang."]
                    
                    if murojaat.type == "application/pdf":
                        reader = PdfReader(io.BytesIO(murojaat.read()))
                        content.append("Hujjat: " + "".join([p.extract_text() for p in reader.pages]))
                    else:
                        content.append(Image.open(murojaat))
                    
                    if izoh: content.append(f"Izoh: {izoh}")
                    
                    res = model.generate_content(content)
                    st.success("Tayyor!")
                    st.info(res.text)
                except Exception as e:
                    st.error(f"Xato: {e}")
        else:
            st.warning("Fayl yuklang!")

# --- MENYU: HISOBOT ---
elif menu == "Hisobot":
    st.title("📊 МФЙлар бўйиcha ҳисобот (Статистика)")
    
    # Namuna uchun jadval yaratish (Rasm-4 dagi kabi)
    data = {
        "МФЙлар Рўйхати": ["Абдужалилбоб", "Ахмад яссавий", "Зарафшон", "Намуна", "Харакат"],
        "Газ": [2, 2, 1, 0, 3],
        "Свет": [2, 2, 1, 1, 2],
        "Сув": [1, 2, 2, 1, 1],
        "Бошқа": [1, 0, 1, 2, 0]
    }
    df = pd.DataFrame(data)
    
    # Jami qatorini qo'shish
    df.loc['jami'] = df.iloc[:, 1:].sum()
    df.at['jami', 'МФЙлар Рўйхати'] = "ТУМАН ЖАМИ"
    
    st.table(df)
    
    st.download_button("📥 Hisobotni Excelda yuklab olish", df.to_csv(), "hisobot.csv")
