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
    .stRadio > div { gap: 20px; }
    </style>
    """, unsafe_allow_html=True)
# 2. API Sozlamasi (AVTOMATIK MODEL QIDIRUVCHI VARIANT)
if "GEMINI_API_KEY" in st.secrets:
    try:
        genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
        
        # Mavjud modellarni tekshirish va ishlaydiganini topish
        available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        
        # Eng yaxshi modellarni ketma-ketlikda qidiramiz
        target_models = ['models/gemini-1.5-flash', 'models/gemini-1.5-pro', 'models/gemini-pro']
        
        selected_model_name = None
        for target in target_models:
            if target in available_models:
                selected_model_name = target
                break
        
        if not selected_model_name:
            # Agar yuqoridagilar topilmasa, ro'yxatdagi birinchi modelni olamiz
            selected_model_name = available_models[0] if available_models else 'gemini-pro'

        model = genai.GenerativeModel(selected_model_name)
        # st.info(f"Ishlatilayotgan model: {selected_model_name}") # Bu qatorni test uchun ochishingiz mumkin
        
    except Exception as e:
        st.error(f"API ulanishda xato: {e}")
        st.stop()
else:
    st.error("Secrets bo'limida API kalit topilmadi!")
    st.stop()
# 3. Sidebar (Faqat Menyu)
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
    st.subheader("Asosiy oyna")

    st.write("📄 Hujjat turini tanlang va asosiy faylni yuklang.")
    hujjat_turi = st.radio("", ["Javob xati", "Ma'lumotnoma", "Yig'ilish bayoni", "Dalolatnoma", "Bildirishnoma"], horizontal=True)
    
    murojaat = st.file_uploader("📥 Asosiy faylni yuklang (PDF yoki Rasm):", type=['png', 'jpg', 'jpeg', 'pdf'])

    # Fayl yuklangandan keyin Mas'ul rahbar va qo'shimcha maydonlar chiqadi
    if murojaat:
        st.markdown("---")
        col1, col2 = st.columns(2)
        
        with col1:
            rahbar = st.selectbox("👤 Mas'ul rahbarn tanlang:", positions)
            ilova = st.file_uploader("📎 Dalolatnoma yoki ma'lumotnoma (ixtiyoriy):", type=['png', 'jpg', 'jpeg', 'pdf'])
        
        with col2:
            izoh = st.text_area("✍️ Qo'shimcha ko'rsatma (Ixtiyoriy):", placeholder="Masalan: Arizani qanoatlantirish haqida...", height=120)

        if st.button("🚀 HUJJATNI TAYYORLASH"):
            with st.spinner("⏳ AI tahlil qilmoqda..."):
                try:
                    prompt = f"Siz {rahbar}siz. Yuklangan hujjat asosida professional '{hujjat_turi}' tayyorlang. Lotin alifbosida, rasmiy uslubda bo'lsin. MFY nomini avtomatik yozmang."
                    content = [prompt]
                    
                    if murojaat.type == "application/pdf":
                        reader = PdfReader(io.BytesIO(murojaat.read()))
                        content.append("Hujjat matni: " + "".join([p.extract_text() for p in reader.pages]))
                    else:
                        content.append(Image.open(murojaat))
                    
                    if izoh: content.append(f"Izoh: {izoh}")
                    
                    res = model.generate_content(content)
                    st.success("✅ Tayyorlandi!")
                    st.markdown("### 📄 Hujjat matni:")
                    st.info(res.text)
                    st.download_button("📥 Nusxalash (.txt)", res.text, file_name=f"{hujjat_turi}.txt")
                except Exception as e:
                    st.error(f"Xato: {e}")

# --- MENYU: MUAMMOLAR TAHLILI (HISOBOT) ---
elif menu == "Muammolar tahlili (Hisobot)":
    st.title("📊 Murojaatlardagi muammolar tahlili")
    st.write("Tuman bo'yicha kelib tushgan murojaatlarning yo'nalishlar kesimidagi statistikasi.")

    # MFYlarsiz, faqat muammo turlari bo'yicha jadval
    stats_data = {
        "Muammo yo'nalishi": ["Tabiiy gaz ta'minoti", "Elektr energiyasi", "Ichimlik suvi", "Yo'l va infratuzilma", "Moddiy yordam", "Bandlik masalasi", "Boshqa masalalar"],
        "Kelib tushgan": [45, 38, 22, 56, 89, 41, 15],
        "Ijobiy hal etilgan": [30, 25, 15, 20, 75, 30, 10],
        "O'rganilmoqda": [10, 8, 5, 30, 10, 8, 3],
        "Tushuntirish berilgan": [5, 5, 2, 6, 4, 3, 2]
    }
    
    df = pd.DataFrame(stats_data)
    
    # Umumiy hisob (Jami)
    st.markdown("### 📈 Yo'nalishlar bo'yicha umumiy holat")
    st.table(df)

    # Vizual ko'rinish (Oddiy bar chart)
    st.bar_chart(df.set_index("Muammo yo'nalishi")["Kelib tushgan"])
    
    st.download_button("📥 Hisobotni Excelda yuklab olish", df.to_csv(index=False), "muammolar_hisoboti.csv")
