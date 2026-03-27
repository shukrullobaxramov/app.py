import streamlit as st
import google.generativeai as genai
from PIL import Image
from PyPDF2 import PdfReader
import io

# 1. Sahifa sozlamalari
st.set_page_config(page_title="Mahijro AI | Zangiota", page_icon="🏛", layout="wide")

# Maxsus CSS dizayn
st.markdown("""
    <style>
    .stButton>button { width: 100%; border-radius: 8px; background-color: #004a99; color: white; font-weight: bold; }
    .stSelectbox { margin-bottom: 15px; }
    h1 { color: #004a99; border-bottom: 2px solid #004a99; }
    .doc-box { padding: 20px; border-radius: 10px; background-color: #f0f2f6; border-left: 5px solid #004a99; }
    </style>
    """, unsafe_allow_html=True)

# 2. API Sozlamasi (Avtomatik model qidiruvchi)
if "GEMINI_API_KEY" in st.secrets:
    try:
        genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
        available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        target_models = ['models/gemini-1.5-flash', 'models/gemini-1.5-pro', 'models/gemini-pro']
        selected_model_name = next((t for t in target_models if t in available_models), available_models[0])
        model = genai.GenerativeModel(selected_model_name)
    except Exception as e:
        st.error(f"⚠️ API ulanishda xato: {e}")
        st.stop()

# 3. Ma'lumotlar
doc_types = ["Javob xati", "Ma'lumotnoma", "Yig'ilish bayoni", "Dalolatnoma", "Bildirishnoma"]
positions = [
    "1. Mahalla uyushmasi tuman bo'limi boshlig'i",
    "2. Tuman Ichki ishlar bo'limi boshlig'i",
    "3. 'Inson' markazi direktori",
    "4. Yoshlar ishlari agentligi boshlig'i",
    "5. Soliq qo'mitasi bo'limi boshlig'i",
    "6. Oila va xotin-qizlar bo'limi boshlig'i",
    "7. Mahallabay ishlash agentligi boshlig'i"
]
mfy_list = sorted(["Abdujalilbob", "Alimbuva", "Amir Temur", "Asil", "Axilobod", "Ahmad Yassaviy", "Baliqchi", "Bog'zor", "Bog'ishamol", "Bodomzor", "Bo'ston", "Gulbog'", "Daligazar", "Dehqonobod", "Zarafshon", "Ilg'or", "Istiqlol", "Katta chinor", "Keng kechik", "Qahramon", "Quyoshli", "Qurilish", "M.M.Xorazmiy", "Madaniyat", "Mevazor", "Navbahor", "Navqiron", "Nazarbek", "Nayman", "Namuna", "Nurafshon", "Nurobod", "Obod", "Olmazor", "Ramadon", "Saxovat", "Sortepa", "Tariq-teshar", "Tarnov", "Tokzor", "To'qimachi", "Turkiston", "Turopobod", "O'ratepa", "O'rikzor", "O'rta", "O'rtaovul", "Fayz", "Farobiy", "Harakat", "Xo'jamozor", "Chinor", "Shodlik", "Erkin", "Eski qala", "Eshonguzar", "Yangi bo'zsuv"])

# 4. Yon Panel (Statistika va Rahbar)
with st.sidebar:
    st.image("https://upload.wikimedia.org/wikipedia/commons/7/77/Emblem_of_Uzbekistan.png", width=80)
    st.title("Boshqaruv")
    rahbar = st.selectbox("👤 Mas'ul rahbar:", positions)
    
    st.markdown("---")
    st.subheader("📊 Statistika uchun")
    mfy_stat = st.selectbox("🏘 Mahalla (MFY):", mfy_list)
    st.caption(f"Hozirda {mfy_stat} MFY bo'yicha ish yuritilmoqda.")

# 5. Asosiy Oyna
st.title("🏛 Mahijro AI: Zangiota tumani")
st.write("Hujjat turini tanlang va faylni yuklang.")

col1, col2 = st.columns([1, 1])

with col1:
    hujjat_turi = st.radio("📄 Hujjat turi:", doc_types, horizontal=True)
    murojaat = st.file_uploader("📥 Asosiy faylni yuklang (Rasm/PDF):", type=['png', 'jpg', 'jpeg', 'pdf'])

with col2:
    izoh = st.text_area("✍️ Qo'shimcha ko'rsatma (Ixtiyoriy):", 
                        placeholder="Masalan: Arizani rad etish sababini tushuntiring...", height=150)

st.markdown("---")

# 6. Generatsiya
if st.button(f"🚀 {hujjat_turi.upper()} TAYYORLASH"):
    if murojaat:
        with st.spinner("⏳ AI hujjatni shakllantirmoqda..."):
            try:
                prompt = f"""Siz {rahbar}siz. Yuklangan fayl asosida professional '{hujjat_turi}' tayyorlang. 
                Hujjat {mfy_stat} mahallasiga tegishli. 
                Talablar:
                1. Faqat lotin alifbosida yozing.
                2. Rasmiy ish yuritish uslubiga rioya qiling.
                3. O'zbekiston Respublikasi qonunchiligiga mos bo'lsin.
                4. Agar bu javob xati bo'lsa, fuqaroga tushunarli va aniq javob bering."""
                
                content = [prompt]
                
                if murojaat.type == "application/pdf":
                    reader = PdfReader(io.BytesIO(murojaat.read()))
                    pdf_text = "".join([p.extract_text() for p in reader.pages])
                    content.append(f"Hujjat matni: {pdf_text}")
                else:
                    content.append(Image.open(murojaat))
                
                if izoh:
                    content.append(f"Qo'shimcha ko'rsatma: {izoh}")

                res = model.generate_content(content)
                
                st.success(f"✅ {hujjat_turi} loyihasi tayyor!")
                st.markdown(f"### 📑 {hujjat_turi} matni:")
                st.info(res.text)
                
                # Yuklab olish imkoniyati
                st.download_button("📥 Matnni nusxalash (.txt)", res.text, file_name=f"{hujjat_turi.replace(' ', '_')}.txt")
                
            except Exception as e:
                st.error(f"❌ Xatolik: {e}")
    else:
        st.warning("⚠️ Iltimos, avval faylni yuklang.")

st.sidebar.markdown("---")
st.sidebar.caption("© 2026 Zangiota tumani Mahijro AI")
