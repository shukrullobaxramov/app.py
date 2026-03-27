import streamlit as st
from PIL import Image

# 1. Sahifa sozlamalari
st.set_page_config(page_title="Mahalla Ijro | Zangiota", page_icon="🏛", layout="wide")

# 2. Maxsus dizayn
st.markdown("""
    <style>
    /* Umumiy fon */
    .stApp { 
        background: linear-gradient(135deg, #f0f9f4, #d9f0c3); 
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        padding: 20px;
    }

    /* Sidebar dizayni */
    [data-testid="stSidebar"] {
        background-color: #e2efda;
        padding: 20px;
        border-radius: 15px;
    }

    /* Header ranglari */
    h1, h2, h3 {
        color: #385723;
    }

    /* Button dizayni */
    .stButton>button { 
        width: 100%; 
        border-radius: 10px; 
        background-color: #70ad47; 
        color: white; 
        border: none; 
        font-weight: bold;
        padding: 10px;
        font-size: 16px;
        transition: 0.3s;
    }

    .stButton>button:hover {
        background-color: #385723;
        color: #fff;
    }

    /* Input maydonlari */
    .stTextInput>div>div>input, 
    .stTextArea>div>div>textarea, 
    .stSelectbox>div>div>div>select, 
    .stFileUploader>div>div>input {
        border-radius: 8px;
        border: 1px solid #b6d7a8;
        padding: 8px;
    }

    /* Radio button spacing */
    .stRadio>div { gap: 20px; }
    </style>
""", unsafe_allow_html=True)

# 3. Sidebar
with st.sidebar:
    st.image("https://upload.wikimedia.org/wikipedia/commons/7/77/Emblem_of_Uzbekistan.png", width=80)
    st.markdown("### 📋 МЕНЮ")
    menu = st.radio("", ["Javob xati yozish", "Muammolar tahlili (Hisobot)"], label_visibility="collapsed")

# 4. Main content
if menu == "Javob xati yozish":
    st.title("🏛 MAHALLA IJRO Zangiota tumani")
    st.subheader("Asosiy oyna")

    st.write("📄 Hujjat turini tanlang va asosiy faylni yuklang.")
    hujjat_turi = st.radio("", ["Javob xati", "Ma'lumotnoma", "Yig'ilish bayoni", "Dalolatnoma", "Bildirishnoma"], horizontal=True)
    
    murojaat = st.file_uploader("📥 Asosiy faylni yuklang (PDF yoki Rasm):", type=['png', 'jpg', 'jpeg', 'pdf'])
    
    st.markdown("---")
    col1, col2 = st.columns(2)
    
    with col1:
        positions = [
            "1. Mahalla uyushmasi tuman bo'limi boshlig'i",
            "2. Tuman Ichki ishlar bo'limi boshlig'i",
            "3. 'Inson' ijtimoiy xizmatlar markazi direktori",
            "4. Yoshlar ishlari agentligi tuman bo'limi boshlig'i",
            "5. Soliq qo'mitasi tuman bo'limi boshlig'i",
            "6. Oila va xotin-qizlar qo'mitasi tuman bo'limi boshlig'i",
            "7. Mahallabay ishlash agentligi boshlig'i"
        ]
        rahbar = st.selectbox("👤 Mas'ul rahbarn tanlang:", positions)
        ilova = st.file_uploader("📎 Dalolatnoma yoki ma'lumotnoma (ixtiyoriy):", type=['png', 'jpg', 'jpeg', 'pdf'])
    
    with col2:
        izoh = st.text_area("✍️ Qo'shimcha ko'rsatma (Ixtiyoriy):", placeholder="Masalan: Arizani qanoatlantirish haqida...", height=120)

    st.button("🚀 HUJJATNI TAYYORLASH")

elif menu == "Muammolar tahlili (Hisobot)":
    st.title("📊 Murojaatlardagi muammolar tahlili")
    st.write("Tuman bo'yicha kelib tushgan murojaatlarning yo'nalishlar kesimidagi statistikasi.")
    
    # Misol jadval
    import pandas as pd
    stats_data = {
        "Muammo yo'nalishi": ["Tabiiy gaz ta'minoti", "Elektr energiyasi", "Ichimlik suvi", "Yo'l va infratuzilma", "Moddiy yordam", "Bandlik masalasi", "Boshqa masalalar"],
        "Kelib tushgan": [45, 38, 22, 56, 89, 41, 15]
    }
    df = pd.DataFrame(stats_data)
    
    st.table(df)
    st.bar_chart(df.set_index("Muammo yo'nalishi")["Kelib tushgan"])
