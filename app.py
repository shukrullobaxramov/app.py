import streamlit as st
import google.generativeai as genai
from PIL import Image
from PyPDF2 import PdfReader
import pandas as pd

st.set_page_config(page_title="Mahijro AI", page_icon="🏛")
st.title("🏛 Mahijro AI")

# Secrets-dan kalitni olish
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
else:
    st.error("API kalit topilmadi! Streamlit Settings -> Secrets bo'limiga GEMINI_API_KEY ni kiriting.")
    st.stop()

tab1, tab2, tab3 = st.tabs(["✍️ Murojaat yuklash", "📊 Mahallalar hisoboti", "🔄 Qayta murojaatlar"])

with tab1:
    uploaded_file = st.file_uploader("Faylni tanlang (Rasm yoki PDF)", type=['png', 'jpg', 'jpeg', 'pdf'])
    
    if st.button("Javob xati tayyorlash"):
        if uploaded_file:
            try:
                model = genai.GenerativeModel('gemini-1.5-flash')
                if uploaded_file.type == "application/pdf":
                    reader = PdfReader(uploaded_file)
                    text = "".join([page.extract_text() for page in reader.pages])
                    response = model.generate_content(f"Murojaatga rasmiy javob yoz: {text}")
                else:
                    img = Image.open(uploaded_file)
                    response = model.generate_content(["Ushbu rasmdagi murojaatga rasmiy javob yoz:", img])
                
                st.success("Tayyorlangan javob:")
                st.write(response.text)
            except Exception as e:
                st.error(f"Xatolik: {e}")
        else:
            st.warning("Fayl yuklanmadi.")

with tab2:
    st.subheader("60 ta mahalla statistikasi")
    df = pd.DataFrame({"Mahalla": [f"{i}-mahalla" for i in range(1, 61)], "Holat": ["Yangi"] * 60})
    st.dataframe(df, use_container_width=True)
