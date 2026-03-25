# -*- coding: utf-8 -*-
import streamlit as st
import google.generativeai as genai
from PIL import Image
from PyPDF2 import PdfReader
import io

# 1. Sahifa sozlamalari va Dizayn
st.set_page_config(page_title="Mahijro AI | Xat Generator", page_icon="🏛", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .stButton>button { width: 100%; border-radius: 10px; height: 3em; background-color: #007bff; color: white; }
    .stTextArea textarea { border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True)

# 2. Login tizimi
if "logged_in" not in st.session_state:
    st.markdown("<h2 style='text-align: center;'>🏛 Mahijro AI: Tizimga kirish</h2>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 1.5, 1])
    with col2:
        u = st.text_input("Login:")
        p = st.text_input("Parol:", type="password")
        if st.button("Kirish"):
            if u == "admin" and p == "zangiota2026":
                st.session_state["logged_in"] = True
                st.rerun()
            else:
                st.error("Login yoki parol xato!")
    st.stop()

# 3. API Sozlamalari (404 xatosini oldini olish uchun barqaror model nomi)
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    # Muhim: Model nomi v1beta-siz, to'g'ridan-to'g'ri chaqirilmoqda
    model = genai.GenerativeModel('gemini-1.5-flash')
else:
    st.error("API kalit topilmadi! Streamlit Secrets bo'limini tekshiring.")
    st.stop()

# 4. Asosiy Interfeys
st.title("🏛 Mahijro AI: Rasmiy javob xati generatori")
st.info("Ushbu tizim murojaat va o'rganish ma'lumotlari asosida tayyor javob loyihasini lotin alifbosida shakllantiradi.")
st.markdown("---")

col_left, col_right = st.columns([1, 1])

with col_left:
    st.subheader("1. Murojaatni yuklang")
    murojaat_file = st.file_uploader("Fuqaro arizasi (PDF yoki Rasm)", type=['png', 'jpg', 'jpeg', 'pdf'], key="m_file")

with col_right:
    st.subheader("2. O'rganish ma'lumotlari")
    organish_file = st.file_uploader("Dalolatnoma/Ma'lumotnoma (Ixtiyoriy)", type=['png', 'jpg', 'jpeg', 'pdf'], key="o_file")
    organish_matni = st.text_area("Qo'shimcha izoh yoki joyidagi holat (Ixtiyoriy):", 
                                 placeholder="Masalan: Murojaat joyiga borib o'rganildi, haqiqatdan ham simyog'och yiqilgan...", height=110)

# 5. Mantiqiy jarayon (AI tahlili)
if st.button("🚀 Javob xati loyihasini shakllantirish"):
    if murojaat_file:
        with st.spinner("Hujjatlar tahlil qilinmoqda va javob yozilmoqda..."):
            try:
                # Promptni shakllantirish
                prompt = """Siz O'zbekistondagi davlat tashkiloti (masalan, Mahalla fuqarolar yig'ini) mas'ul xodimisiz. 
                Vazifangiz: Yuklangan murojaatni va (agar mavjud bo'lsa) o'rganish ma'lumotlarini tahlil qilib, 
                fuqaroga rasmiy, qonuniy asoslangan va savodli javob xati loyihasini tayyorlash.
                
                TALABLAR:
                1. Javob xati LOTIN alifbosida, rasmiy ish yuritish uslubida bo'lsin.
                2. Murojaatdagi muammoni va o'rganish ma'lumotlaridagi faktlarni aniq ko'rsating.
                3. Agar o'rganish ma'lumotlari berilmagan bo'lsa, umumiy tartibda ko'rib chiqilgani haqida yozing.
                4. Javob xati oxirida 'Hurmat bilan, [Mas'ul xodim ismi]' deb qoldiring.
                """
                
                input_data = [prompt]
                
                # Murojaatni qayta ishlash
                if murojaat_file.type == "application/pdf":
                    pdf_reader = PdfReader(muro_file := io.BytesIO(murojaat_file.read()))
                    m_text = "".join([page.extract_text() for page in pdf_reader.pages])
                    input_data.append(f"MUROJAAT MATNI: {m_text}")
                else:
                    input_data.append(Image.open(murojaat_file))
                
                # O'rganish ma'lumotlarini qo'shish
                if organish_matni:
                    input_data.append(f"O'RGANISH NATIJASI (IZOH): {organish_matni}")
                
                if organish_file:
                    if organish_file.type == "application/pdf":
                        pdf_reader_o = PdfReader(org_file := io.BytesIO(organish_file.read()))
                        o_text = "".join([page.extract_text() for page in pdf_reader_o.pages])
                        input_data.append(f"DALOLATNOMA MATNI: {o_text}")
                    else:
                        input_data.append(Image.open(organish_file))

                # AI generatsiyasi
                response = model.generate_content(input_data)
                
                st.success("✅ Javob xati loyihasi tayyor!")
                st.markdown("---")
                st.markdown(response.text)
                st.info("💡 Yuqoridagi matnni nusxalab, Word faylga o'tkazishingiz mumkin.")
                
            except Exception as e:
                st.error(f"Xatolik yuz berdi: {str(e)}")
    else:
        st.warning("Iltimos, avval murojaat faylini (ariza) yuklang.")

st.markdown("---")
st.caption("© 2026 Mahijro AI - Zangiota tumani mahalla tizimi uchun maxsus.")
