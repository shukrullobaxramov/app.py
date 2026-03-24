import streamlit as st
from google import genai
from PIL import Image
from PyPDF2 import PdfReader
import pandas as pd

st.set_page_config(page_title="Mahijro AI", page_icon="🏛")
st.title("🏛 Mahijro AI")

# Secrets-dan kalitni olish
if "GEMINI_API_KEY" in st.secrets:
    client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])
else:
    st.error("API kalit topilmadi! Secrets bo'limini tekshiring.")
    st.stop()

tab1, tab2, tab3 = st.tabs(["✍️ Мурожаат юклаш", "📊 Маҳаллалар ҳисоботи", "🔄 Қайта мурожаатлар"])

with tab1:
    st.subheader("Мурожаатни юкланг (Расм ёки PDF)")
    uploaded_file = st.file_uploader("Файлни танланг", type=['png', 'jpg', 'jpeg', 'pdf'])
    murojaat_izoh = st.text_area("Мурожаат бўйича қўшимча изоҳ ёки матнни киритинг:", height=150)
    
    if st.button("Жавоб хати тайёрлаш"):
        if uploaded_file or murojaat_izoh:
            with st.spinner("AI таҳлил қилмоқда..."):
                try:
                    content_list = []
                    prompt = "Сиз давлат идораси ходимисиз. Қуйидаги мурожаатни ўрганиб чиқиб, расмий ва қонуний жавоб хати лойиҳасини ўзбек тилида тайёрлаб беринг:"
                    content_list.append(prompt)
                    
                    if murojaat_izoh:
                        content_list.append(f"\nҚўшимча изоҳ: {murojaat_izoh}")
                    
                    if uploaded_file:
                        if uploaded_file.type == "application/pdf":
                            reader = PdfReader(uploaded_file)
                            pdf_text = "".join([page.extract_text() for page in reader.pages])
                            content_list.append(f"\nPDF матни: {pdf_text}")
                        else:
                            img = Image.open(uploaded_file)
                            content_list.append(img)

                    # Yangi kutubxona bo'yicha chaqirish
                    response = client.models.generate_content(
                        model="gemini-2.0-flash",
                        contents=content_list
                    )
                    
                    st.success("Тайёрланган жавоб:")
                    st.write(response.text)
                except Exception as e:
                    st.error(f"Хатолик юз берди: {str(e)}")
        else:
            st.warning("Файл юкланг ёки матн киритинг.")

with tab2:
    st.subheader("60 та маҳалла статистикаси")
    df = pd.DataFrame({"Маҳалла": [f"{i}-маҳалла" for i in range(1, 61)], "Ҳолат": ["Янги"] * 60})
    st.dataframe(df, use_container_width=True)
