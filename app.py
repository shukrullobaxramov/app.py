import streamlit as st
import google.generativeai as genai
from PIL import Image
from PyPDF2 import PdfReader
import io
import pandas as pd

# 1. Sahifa sozlamalari
st.set_page_config(page_title="Mahalla Ijro | Zangiota", page_icon="🏛", layout="wide")

# --- LOGIN TIZIMI ---
def check_password():
    if "password_correct" not in st.session_state:
        st.session_state["password_correct"] = False

    if st.session_state["password_correct"]:
        return True

    # Kirish oynasi dizayni (To'liq lotincha)
    st.markdown("<h1 style='text-align: center; color: #385723;'>🏛 Mahalla Ijro Tizimi</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center;'>Tizimga kirish uchun login va parolni kiriting</p>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        username = st.text_input("Login")
        password = st.text_input("Parol", type="password")
        if st.button("Kirish"):
            creds = st.secrets.get("credentials", {})
            if username in creds and str(creds[username]) == password:
                st.session_state["password_correct"] = True
                st.rerun()
            else:
                st.error("❌ Login yoki parol noto'g'ri!")
    return False

if not check_password():
    st.stop()

# --- ASOSIY DASTUR ---
# API Sozlamasi (AVTOMATIK MODEL QIDIRUVCHI VARIANT)
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


# Sidebar Menyu (Lotincha)
with st.sidebar:
    st.image("https://upload.wikimedia.org/wikipedia/commons/7/77/Emblem_of_Uzbekistan.png", width=80)
    st.markdown("### 📋 MENYU")
    menu = st.radio("", ["Javob xati yozish", "Muammolar tahlili"], label_visibility="collapsed")
    st.markdown("---")
    if st.button("Chiqish"):
        st.session_state["password_correct"] = False
        st.rerun()

# Mas'ul rahbarlar ro'yxati (Lotincha)
positions = [
    "1. Mahallalar uyushmasi tuman bo'limi boshlig'i",
    "2. Tuman Ichki ishlar bo'limi boshlig'i",
    "3. 'Inson' ijtimoiy xizmatlar markazi direktori",
    "4. Yoshlar ishlari agentligi tuman bo'limi boshlig'i",
    "5. Soliq qo'mitasi tuman bo'limi boshlig'i",
    "6. Oila va xotin-qizlar qo'mitasi tuman bo'limi boshlig'i",
    "7. Kambag‘allikni qisqartirish va bandlik bo‘limi boshlig'i"
]

if menu == "Javob xati yozish":
    st.title("🏛 MAHALLA IJRO | Zangiota")
    st.subheader("Asosiy oyna")
    
    hujjat_turi = st.radio("📄 Hujjat turi:", ["Javob xati", "Ma'lumotnoma", "Yig'ilish bayoni", "Dalolatnoma"], horizontal=True)
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
                    prompt = f"Siz {rahbar}siz. '{hujjat_turi}' tayyorlang. Faqat lotin alifbosida, rasmiy uslubda bo'lsin. Mahalla nomini o'zingizdan qo'shmang."
                    content = [prompt]
                    if murojaat.type == "application/pdf":
                        reader = PdfReader(io.BytesIO(muro_read := murojaat.read()))
                        content.append("Matn: " + "".join([p.extract_text() for p in reader.pages]))
                    else:
                        content.append(Image.open(murojaat))
                    if izoh: content.append(f"Ko'rsatma: {izoh}")
                    
                    res = model.generate_content(content)
                    st.success("✅ Loyiha tayyorlandi!")
                    st.markdown("### 📄 Hujjat matni:")
                    st.info(res.text)
                    st.download_button("📥 Matnni yuklab olish (.txt)", res.text, file_name=f"{hujjat_turi}.txt")
                except Exception as e:
                    st.error(f"Xatolik: {e}")

elif menu == "Muammolar tahlili":
    st.title("📊 Yo'nalishlar bo'yicha tahlil")
    st.write("Murojaatlardagi asosiy muammolar statistikasi")
    
    stats_data = {
        "Muammo yo'nalishi": ["Tabiiy gaz", "Elektr energiyasi", "Ichimlik suvi", "Yo'l va infratuzilma", "Moddiy yordam", "Bandlik", "Boshqa"],
        "Soni": [45, 38, 22, 56, 89, 41, 15]
    }
    df = pd.DataFrame(stats_data)
    st.table(df)
    st.bar_chart(df.set_index("Muammo yo'nalishi"))
