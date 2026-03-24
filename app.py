import streamlit as st
from google import genai
from PIL import Image
from PyPDF2 import PdfReader
import pandas as pd

# 1. Sahifa va Dizayn sozlamalari
st.set_page_config(page_title="Mahijro AI", page_icon="🏛", layout="wide")

# 2. Login tizimi (Foydalanuvchilar ro'yxati)
def login():
    st.markdown("<h2 style='text-align: center;'>🏛 Mahijro AI: Tizimga kirish</h2>", unsafe_allow_html=True)
    
    # Bu yerga yangi xodimlarni login va parolini qo'shishingiz mumkin
    users = {
        "admin": "zangiota2026",
        "rahbar": "zangiota_boss",
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
                st.error("Login yoki parol xato! Qayta urining.")

# Tizimga kirganlikni tekshirish
if "logged_in" not in st.session_state:
    login()
    st.stop()

# 3. Sidebar (Yon menyu) - Chiqish tugmasi
with st.sidebar:
    st.markdown(f"### 👤 **{st.session_state['user_name'].upper()}**")
    st.write("Lavozimi: Mas'ul xodim")
    if st.button("🚪 Tizimdan chiqish"):
        del st.session_state["logged_in"]
        st.rerun()
    st.markdown("---")
    st.info("Zangiota tumani Mahalla uyushmasi uchun.")

# 4. Asosiy dastur interfeysi
st.title("🏛 Mahijro AI: Zangiota tumani")

# API kalitni Secrets dan olish
if "GEMINI_API_KEY" in st.secrets:
    client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])
else:
    st.error("API kalit topilmadi! Iltimos, Secrets bo'limini tekshiring.")
    st.stop()

# MFY ro'yxati (Siz yuborgan rasmdagi tartibda)
malla_nomlari = [
    "Gulbog'", "Xo'jamazor", "Asil", "O'rta", "Eski qala", "Sortecha", "Bog'zor", "Abdujalilbob", "O'rtaovul", "Obod turmush",
    "Katta chinor", "Olmazor", "Fayz", "Keng kechik", "Eshonguzar", "Amir Temur", "Nurafshon", "Namuna", "Navqiron", "O'ratepa",
    "Daligazar", "Obod", "Tokzor", "Nazarbek", "M.M.Xorazmiy", "Farobiy", "Axilobod", "Nayman", "Ahmad Yassaviy", "Bo'ston",
    "Istiqlolning 5-yilligi", "Bog'ishamol", "Saxovat", "To'qimachi", "Baliqchi", "Tarnov", "Navbahor", "Shodlik", "Alimbuva", "Turopobod",
    "Ramadon", "Ilg'or", "Obod to'qimachi", "Harakat", "Mevazor", "Yangi bo'suz", "Zarafshon", "Nurobod", "Madaniyat", "Dexkonobod",
    "Chinor", "O'rikzor", "Istiqlol", "Erkin", "Qurilish", "Quyoshli", "Tariq-teshar", "Qahramon", "Bodomzor", "Turkiston"
]

tab1, tab2, tab3 = st.tabs(["✍️ Murojaat yuklash", "📊 Mahallalar hisoboti", "🔄 Qayta murojaatlar"])

with tab1:
    st.subheader("Murojaatga javob tayyorlash")
    colA, colB = st.columns([1, 1])
    with colA:
        uploaded_file = st.file_uploader("Murojaatni yuklang (PDF yoki Rasm)", type=['png', 'jpg', 'jpeg', 'pdf'])
        selected_mfy = st.selectbox("Qaysi mahalla mas'uli tayyorlaydi?", malla_nomlari)
    with colB:
        murojaat_izoh = st.text_area("Qo'shimcha izoh yoki topshiriqni yozing:", height=150)
    
    if st.button("📝 Javob xati loyihasini yaratish", use_container_width=True):
        if uploaded_file or murojaat_izoh:
            with st.spinner("AI tahlil qilmoqda..."):
                try:
                    prompt = f"Siz Zangiota tumani {selected_mfy} MFY raisisiz. Quyidagi murojaatga rasmiy, qonuniy va xushmuomala javob xati loyihasini tayyorlang:"
                    content_list = [prompt]
                    if murojaat_izoh: content_list.append(f"Qo'shimcha ko'rsatma: {murojaat_izoh}")
                    
                    if uploaded_file:
                        if uploaded_file.type == "application/pdf":
                            pdf_text = "".join([p.extract_text() for p in PdfReader(uploaded_file).pages])
                            content_list.append(f"Hujjat matni: {pdf_text[:4000]}")
                        else:
                            content_list.append(Image.open(uploaded_file))

                    response = client.models.generate_content(model="gemini-1.5-flash", contents=content_list)
                    st.success("Tayyorlangan javob loyihasi:")
                    st.write(response.text)
                except Exception as e:
                    st.error("Xatolik: Limit tugagan bo'lishi mumkin. 1 daqiqa kutib qayta urining.")
        else:
            st.warning("Iltimos, fayl yuklang yoki izoh yozing.")

with tab2:
    st.subheader("60 ta MFY kesimida nazorat")
    data = {"№": range(1, 61), "MFY nomi": malla_nomlari, "Kelgan": [0]*60, "Bajarilgan": [0]*60}
    st.dataframe(pd.DataFrame(data), use_container_width=True, hide_index=True)

with tab3:
    st.info("🔄 Bu bo'limda bir xil fuqarodan kelgan takroriy murojaatlar tahlil qilinadi.")
