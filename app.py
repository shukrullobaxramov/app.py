# -*- coding: utf-8 -*-
import streamlit as st
import google.generativeai as genai
from PIL import Image

# 1. Sahifa sozlamalari
st.set_page_config(page_title="Mahijro AI", page_icon="🏛", layout="wide")

# 2. Login tizimi
def login():
    st.markdown("<h2 style='text-align: center;'>🏛 Mahijro AI: Tizimga kirish</h2>", unsafe_allow_html=True)
    users = {
        "admin": "zangiota2026",
        "shukrullo": "zangiota_777"
    }
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        username = st.text_input("Loginingizni kiriting:")
        password = st.text_input("Maxfiy parolni kiriting:", type="password")
        if st.button("Kirish", use_container_width=True):
            if username in users and users[username] == password:
                st.session_state["logged_in"] = True
                st.session_state["user_name"] = username
                st.rerun()
            else:
                st.error("Login yoki parol xato!")

if "logged_in" not in st.session_state:
    login()
    st.stop()

# 3. Sidebar (Yon menyu)
with st.sidebar:
    st.markdown(f"### 👤 {st.session_state['user_name'].upper()}")
    if st.button("🚪 Tizimdan chiqish"):
        del st.session_state["logged_in"]
        st.rerun()
    st.markdown("---")
    st.info("Zangiota tumani Mahalla uyushmasi")

# 4. API sozlamalari
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
else:
    st.error("API kalit topilmadi! Secrets bo'limini tekshiring.")
    st.stop()

model = genai.GenerativeModel('gemini-1.5-flash')

# 5. MFY ro'yxati (ALIFBO TARTIBIDA)
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

# 6. Asosiy interfeys
st.title("🏛 Mahijro AI: Ishchi paneli")

tab1, tab2 = st.tabs(["✍️ Murojaat tahlili", "📊 MFY hisoboti"])

with tab1:
    st.subheader("Murojaatga javob tayyorlash")
    colA, colB = st.columns([1, 1])
    with colA:
        uploaded_file = st.file_uploader("Murojaatni yuklang (Rasm)", type=['png', 'jpg', 'jpeg'])
        selected_mfy = st.selectbox("Mahallani tanlang:", malla_nomlari)
    with colB:
        murojaat_izoh = st.text_area("Rezolyutsiya yoki qo'shimcha izoh:", height=100)
    
    if st.button("📝 Javob xati loyihasini yaratish", use_container_width=True):
        if uploaded_file or murojaat_izoh:
            with st.spinner("AI tahlil qilmoqda..."):
                try:
                    prompt = f"Siz Zangiota tumani {selected_mfy} MFY raisisiz. Rasmiy javob xati loyihasini tayyorlang."
                    content = [prompt]
                    if murojaat_izoh: content.append(f"Izoh: {murojaat_izoh}")
                    if uploaded_file: content.append(Image.open(uploaded_file))

                    response = model.generate_content(content)
                    st.success("Tayyorlangan javob:")
                    st.write(response.text)
                except Exception as e:
                    st.error("Hozir band. 1 daqiqa kutib qayta urinib ko'ring (Limit tugagan).")
        else:
            st.warning("Fayl yuklang yoki matn kiriting.")

with tab2:
