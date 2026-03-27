import streamlit as st
import google.generativeai as genai
from PIL import Image
from PyPDF2 import PdfReader
import io

# 1. Sahifa sozlamalari
st.set_page_config(page_title="Mahijro AI | Zangiota", page_icon="🏛", layout="wide")
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
# 3. Ma'lumotlar bazasi (7 ta Rahbar va 60 ta MFY)
positions = [
    "1. Mahalla uyushmasi tuman bo'limi boshlig'i",
    "2. Tuman Ichki ishlar bo'limi boshlig'i",
    "3. 'Inson' ijtimoiy xizmatlar markazi direktori",
    "4. Yoshlar ishlari agentligi tuman bo'limi boshlig'i",
    "5. Soliq qo'mitasi tuman bo'limi boshlig'i",
    "6. Oila va xotin-qizlar qo'mitasi tuman bo'limi boshlig'i",
    "7. Mahallabay ishlash va tadbirkorlikni rivojlantirish agentligi boshlig'i"
]

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

# 4. Interfeys dizayni
st.title("🏛 Mahijro AI: Markaziy Boshqaruv Tizimi")
st.write("Zangiota tumani mas'ul rahbarlari uchun rasmiy hujjatlar generatori.")
st.markdown("---")

col1, col2 = st.columns(2)

with col1:
    selected_rahbar = st.selectbox("Mas'ul rahbar (Lavozim):", positions)
    selected_mfy = st.selectbox("Tegishli mahalla (MFY):", mfy_list)
    murojaat_file = st.file_uploader("Fuqaro murojaati (PDF yoki Rasm):", type=['png', 'jpg', 'jpeg', 'pdf'])

with col2:
    dalolatnoma_file = st.file_uploader("O'rganish dalolatnomasi (Ixtiyoriy):", type=['png', 'jpg', 'jpeg', 'pdf'])
    izoh = st.text_area("Qo'shimcha ko'rsatma yoki izoh:", placeholder="Masalan: Arizani qanoatlantirish haqida...", height=110)

# 5. Generatsiya jarayoni
if st.button("🚀 RASMIY JAVOBNI SHAKLLANTIRISH"):
    if murojaat_file:
        with st.spinner("AI hujjatlarni tahlil qilmoqda, iltimos kuting..."):
            try:
                # Prompt mantiqi
                prompt = f"Siz {selected_rahbar}siz. {selected_mfy} mahallasidan kelgan murojaatni o'rganib chiqib, rasmiy, qonuniy va o'ta savodli javob xati yozing. Matn FAQAT LOTIN alifbosida bo'lsin."
                content = [prompt]
                
                # Murojaatni tahlil qilish
                if murojaat_file.type == "application/pdf":
                    reader = PdfReader(io.BytesIO(murojaat_file.read()))
                    pdf_text = "".join([page.extract_text() for page in reader.pages])
                    content.append(f"Murojaat matni: {pdf_text}")
                else:
                    content.append(Image.open(murojaat_file))
                
                # Dalolatnomani qo'shish
                if dalolatnoma_file:
                    if dalolatnoma_file.type == "application/pdf":
                        reader_d = PdfReader(io.BytesIO(dalolatnoma_file.read()))
                        content.append("Dalolatnoma matni: " + "".join([p.extract_text() for p in reader_d.pages]))
                    else:
                        content.append(Image.open(dalolatnoma_file))
                
                if izoh:
                    content.append(f"Qo'shimcha ko'rsatma: {izoh}")

                # AI dan javob olish
                response = model.generate_content(content)
                
                st.success("✅ Rasmiy javob loyihasi tayyor!")
                st.markdown("---")
                st.markdown("### 📄 Tayyorlangan hujjat matni:")
                st.write(response.text)
                
            except Exception as e:
                st.error(f"Xatolik yuz berdi: {str(e)}")
    else:
        st.warning("Iltimos, avval murojaat faylini yuklang.")

st.markdown("---")
st.caption("© 2026 Mahijro AI - Zangiota tumani tahliliy tizimi")
