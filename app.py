import streamlit as st
import google.generativeai as genai
from PIL import Image
import pandas as pd
from PyPDF2 import PdfReader

# Sahifa sozlamalari
st.set_page_config(page_title="Mahijro AI", page_icon="🏛")
st.title("🏛 Mahijro AI")

# API kalitni ulash (Xatolikni oldini olish uchun)
if "GEMINI_API_KEY" not in st.secrets:
    st.error("API kalit topilmadi! Iltimos, Secrets bo'limiga GEMINI_API_KEY ni kiriting.")
    st.stop()

genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

tab1, tab2, tab3 = st.tabs(["✍️ Murojaat yuklash", "📊 Mahallalar hisoboti", "🔄 Qayta murojaatlar"])

with tab1:
    uploaded_file = st.file_uploader("Faylni tanlang (Rasm yoki PDF)", type=['png', 'jpg', 'jpeg', 'pdf'])
    
    if st.button("Javob xati tayyorlash"):
        if uploaded_file:
            with st.spinner("AI tahlil qilmoqda..."):
                model = genai.GenerativeModel('gemini-1.5-flash')
                
                if uploaded_file.type == "application/pdf":
                    pdf_reader = PdfReader(uploaded_file)
                    text = "".join([page.extract_text() for page in pdf_reader.pages])
                    response = model.generate_content(f"Quyidagi murojaatga rasmiy javob yoz: {text}")
                else:
                    img = Image.open(uploaded_file)
                    response = model.generate_content(["Ushbu rasmdagi murojaatga rasmiy javob yoz:", img])
                
                st.success("Tayyorlangan javob:")
                st.write(response.text)
        else:
            st.warning("Iltimos, fayl yuklang.")

with tab2:
    st.subheader("60 ta mahalla statistikasi")
    df = pd.DataFrame({"Mahalla": [f"{i}-mahalla" for i in range(1, 61)], "Holat": ["Yangi"] * 60})
    st.dataframe(df, use_container_width=True)
