import streamlit as st
from google import genai
from PIL import Image
import os

# Саҳифа созламалари
st.set_page_config(page_title="Mahijro AI", page_icon="🏛", layout="centered")

# Дизайн ва Сарлавҳа
st.markdown("<h1 style='text-align: center; color: #1E88E5;'>🏛 Mahijro AI</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>Давлат хизматчилари учун мурожаатларга тезкор ва қонуний жавоб тайёрлаш тизими</p>", unsafe_allow_html=True)

# API калитни хавфсиз олиш (Streamlit Secrets орқали)
try:
    API_KEY = st.secrets["GEMINI_API_KEY"]
    client = genai.Client(api_key=API_KEY)
except:
    st.warning("Тизим созланмоқда. Илтимос, API калитни Secrets бўлимига киритинг.")
    st.stop()

# Парол тизими
if 'auth' not in st.session_state:
    st.session_state['auth'] = False

if not st.session_state['auth']:
    with st.container():
        st.write("---")
        pw = st.text_input("Кириш паролини ёзинг:", type="password")
        if st.button("Тизимга кириш"):
            if pw == "zangiota2026":
                st.session_state['auth'] = True
                st.rerun()
            else:
                st.error("Парол нотўғри!")
else:
    # Асосий ишчи майдон
    st.success("Хуш келибсиз! Мурожаатни таҳлил қилиш учун расмни юкланг.")
    
    file = st.file_uploader("Ҳужжат расмини танланг (PNG, JPG)", type=['png', 'jpg', 'jpeg'])
    
    if file:
        img = Image.open(file)
        st.image(img, caption="Юкланган ҳужжат", use_container_width=True)
        
        if st.button("📜 Жавоб лойиҳасини тайёрлаш"):
            with st.spinner("AI ҳужжатни ўрганмоқда..."):
                prompt = "Analyze this citizen's application image. Write a formal, professional, and legally sound response letter in Uzbek language following official administrative standards of Uzbekistan."
                try:
                    res = client.models.generate_content(model="gemini-1.5-flash", contents=[prompt, img])
                    st.markdown("### ✅ Тайёр жавоб матни:")
                    st.info(res.text)
                    st.download_button("Матнни кўчириб олиш", res.text)
                except Exception as e:
                    st.error(f"Хатолик: {e}")

st.markdown("---")
st.caption("© 2026 Mahijro AI - Барча ҳуқуқлар ҳимояланган.")
