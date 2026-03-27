import streamlit as st
import google.generativeai as genai
from PIL import Image
from PyPDF2 import PdfReader
import io

st.set_page_config(page_title="Mahijro AI", page_icon="🏛", layout="wide")

# 1. API Sozlamasi (Xatosiz versiya)
try:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    st.error(f"API ulanishda xato: {e}")

# 2. Ma'lumotlar
positions = [
    "1. Mahalla uyushmasi tuman bo'limi boshlig'i",
    "2. Tuman Ichki ishlar bo'limi boshlig'i",
    "3. 'Inson' ijtimoiy xizmatlar markazi direktori",
    "4. Yoshlar ishlari agentligi tuman bo'limi boshlig'i",
    "5. Soliq qo'mitasi tuman bo'limi boshlig'i",
    "6. Oila va xotin-qizlar qo'mitasi tuman bo'limi boshlig'i",
    "7. Mahallabay ishlash va tadbirkorlikni rivojlantirish agentligi boshlig'i"
]

mfy_list = ["Abdujalilbob", "Alimbuva", "Amir Temur", "Asil", "Axilobod", "Ahmad Yassaviy", "Baliqchi", "Bog'zor", "Bog'ishamol", "Bodomzor", "Bo'ston", "Gulbog'", "Daligazar", "Dehqonobod", "Zarafshon", "Ilg'or", "Istiqlol", "Istiqlolning 5-yilligi", "Katta chinor", "Keng kechik", "Qahramon", "Quyoshli", "Qurilish", "M.M.Xorazmiy", "Madaniyat", "Mevazor", "Navbahor", "Navqiron", "Nazarbek", "Nayman", "Namuna", "Nurafshon", "Nurobod", "Obod", "Obod to'qimachi", "Obod turmush", "Olmazor", "Ramadon", "Saxovat", "Sortepa", "Tariq-teshar", "Tarnov", "Tokzor", "To'qimachi", "Turkiston", "Turopobod", "O'ratepa", "O'rikzor", "O'rta", "O'rtaovul", "Fayz", "Farobiy", "Harakat", "Xo'jamozor", "Chinor", "Shodlik", "Erkin", "Eski qala", "Eshonguzar", "Yangi bo'zsuv"]

# 3. Interfeys
st.title("🏛 Mahijro AI: Zangiota tumani")
rahbar = st.selectbox("Mas'ul rahbar:", positions)
mfy = st.selectbox("Mahalla:", mfy_list)
murojaat = st.file_uploader("Murojaatni yuklang (PDF/Rasm):", type=['png', 'jpg', 'pdf'])
dalolatnoma = st.file_uploader("Dalolatnoma (Ixtiyoriy):", type=['png', 'jpg', 'pdf'])

if st.button("🚀 Javobni tayyorlash"):
    if murojaat:
        with st.spinner("AI tahlil qilmoqda..."):
            inputs = [f"Siz {rahbar}siz. {mfy} mahallasi uchun rasmiy javob yozing. Lotin alifbosida."]
            if murojaat.type == "application/pdf":
                inputs.append("Arizada shunday yozilgan: " + "".join([p.extract_text() for p in PdfReader(io.BytesIO(murojaat.read())).pages]))
            else:
                inputs.append(Image.open(murojaat))
            res = model.generate_content(inputs)
            st.success("Tayyor!")
            st.write(res.text)
