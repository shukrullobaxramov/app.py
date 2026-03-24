import streamlit as st
from google import genai
from PIL import Image
import pandas as pd

st.set_page_config(page_title="Mahijro AI", page_icon="🏛")
st.title("🏛 Mahijro AI")
st.markdown("##### Мурожаатларга тезкор ва қонуний жавоб тайёрлаш тизими")

if "GEMINI_API_KEY" not in st.secrets:
    st.warning("Тизим созланмоқда. Илтимос, API калитни Secrets бўлимига киритинг.")
    st.stop()

client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])

# Табларни яратамиз
tab1, tab2, tab3 = st.tabs(["✍️ Мурожаат юклаш", "📊 Маҳаллалар ҳисоботи", "🔄 Қайта мурожаатлар"])

with tab1:
    st.subheader("Мурожаатни матн ёки файл кўринишида киритинг")
    
    # Файл юклаш қисми (Расм, PDF, DOCX)
    uploaded_file = st.file_uploader("Мурожаат расми ёки ҳужжатини юкланг", type=['png', 'jpg', 'jpeg', 'pdf', 'docx'])
    
    murojaat_text = st.text_area("Ёки мурожаат матнини бу ерга ёзинг:", height=150)
    
    if st.button("Жавоб хати тайёрлаш"):
        with st.spinner("AI таҳлил қилмоқда..."):
            input_content = []
            if murojaat_text:
                input_content.append(murojaat_text)
            
            if uploaded_file:
                if uploaded_file.type.startswith('image'):
                    img = Image.open(uploaded_file)
                    input_content.append(img)
                else:
                    input_content.append(f"Файл юкланди: {uploaded_file.name}. Илтимос, уни таҳлил қил.")

            if input_content:
                # AI жавоб бериши
                response = client.models.generate_content(
                    model="gemini-2.0-flash",
                    contents=["Сен давлат идораси ходимисан. Қуйидаги мурожаатни (матн ёки расм) Ўзбекистон қонунчилиги асосида ўрганиб чиқ ва расмий жавоб хати лойиҳасини ўзбек тилида тайёрлаб бер:"] + input_content
                )
                st.success("Тайёрланган жавоб:")
                st.write(response.text)
            else:
                st.error("Илтимос, матн ёзинг ёки файл юкланг!")

with tab2:
    st.subheader("60 та маҳалла бўйича таҳлил")
    # Маҳаллалар рўйхати ва статистикаси
    df = pd.DataFrame({
        "Маҳалла номи": [f"Маҳалла {i}" for i in range(1, 61)],
        "Келиб тушган": [0] * 60,
        "Жавоб берилган": [0] * 60
    })
    st.dataframe(df, use_container_width=True)

with tab3:
    st.subheader("🔄 Қайта мурожаатлар назорати")
    st.info("Бу бўлимда тизим мурожаатчининг исми ва мавзуси бўйича қайта келган хатларни аниқлайди.")
