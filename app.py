import streamlit as st
import google.generativeai as genai
from PIL import Image
from PyPDF2 import PdfReader
import pandas as pd

st.set_page_config(page_title="Mahijro AI", page_icon="🏛")
st.title("🏛 Mahijro AI")

# Secrets-дан калитни олиш
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
else:
    st.error("API калит топилмади! Secrets бўлимини текширинг.")
    st.stop()

tab1, tab2, tab3 = st.tabs(["✍️ Мурожаат юклаш", "📊 Маҳаллалар ҳисоботи", "🔄 Қайта мурожаатлар"])

with tab1:
    st.subheader("Мурожаатни юкланг (Расм ёки PDF)")
    uploaded_file = st.file_uploader("Файлни танланг", type=['png', 'jpg', 'jpeg', 'pdf'])
    murojaat_izoh = st.text_area("Мурожаат бўйича қўшимча изоҳ ёки матнни киритинг:", height=150)
    
    if st.button("Жавоб хати тайёрлаш"):
        if uploaded_file or murojaat_izoh:
            try:
                # Энг барқарор моделни чақириш усули
                model = genai.GenerativeModel('gemini-1.5-flash')
                content_parts = []
                
                # Кўрсатма қўшиш
                prompt = "Сен давлат идораси ходимисан. Қуйидаги мурожаатга Ўзбекистон қонунчилиги асосида расмий жавоб хати лойиҳасини ўзбек тилида тайёрла."
                content_parts.append(prompt)
                
                if murojaat_izoh:
                    content_parts.append(f"Изоҳ: {murojaat_izoh}")
                
                if uploaded_file:
                    if uploaded_file.type == "application/pdf":
                        reader = PdfReader(uploaded_file)
                        pdf_text = ""
                        for page in reader.pages:
                            pdf_text += page.extract_text()
                        content_parts.append(f"PDF матни: {pdf_text}")
                    else:
                        img = Image.open(uploaded_file)
                        content_parts.append(img)

                with st.spinner("AI таҳлил қилмоқда..."):
                    # Мана шу ерда форматни тўғирладик
                    response = model.generate_content(content_parts)
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
