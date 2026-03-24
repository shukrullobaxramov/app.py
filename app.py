import streamlit as st
from google import genai
from PIL import Image
import pandas as pd
from PyPDF2 import PdfReader
import io

st.set_page_config(page_title="Mahijro AI", page_icon="🏛")
st.title("🏛 Mahijro AI")
st.markdown("##### Murojaatlarga javob tayyorlash va tahlil tizimi")

if "GEMINI_API_KEY" not in st.secrets:
    st.warning("Tizim sozlanmoqda. API kalitni Secrets bo'limiga kiriting.")
    st.stop()

client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])

tab1, tab2, tab3 = st.tabs(["✍️ Murojaat yuklash", "📊 Mahallalar hisoboti", "🔄 Qayta murojaatlar"])

with tab1:
    st.subheader("Murojaatni matn, rasm yoki PDF ko'rinishida yuklang")
    
    # Fayl yuklash (Rasm va PDF)
    uploaded_file = st.file_uploader("Faylni yuklang (JPG, PNG, PDF)", type=['png', 'jpg', 'jpeg', 'pdf'])
    murojaat_text = st.text_area("Yoki murojaat matnini yozing:", height=100)
    
    if st.button("Javob xati tayyorlash"):
        with st.spinner("AI tahlil qilmoqda..."):
            input_content = []
            prompt = "Siz davlat idorasi xodimisiz. Quyidagi murojaatni (matn, rasm yoki PDF) O'zbekiston qonunchiligi asosida o'rganib chiqib, rasmiy javob xati loyihasini o'zbek tilida tayyorlab bering:"
            input_content.append(prompt)

            if murojaat_text:
                input_content.append(murojaat_text)
            
            if uploaded_file:
                if uploaded_file.type == "application/pdf":
                    # PDF dan matnni ajratib olish
                    pdf_reader = PdfReader(uploaded_file)
                    pdf_text = ""
                    for page in pdf_reader.pages:
                        pdf_text += page.extract_text()
                    input_content.append(f"PDF ichidagi matn: {pdf_text}")
                else:
                    # Rasmni yuklash
                    img = Image.open(uploaded_file)
                    input_content.append(img)

            if len(input_content) > 1:
                try:
                    response = client.models.generate_content(
                        model="gemini-2.0-flash",
                        contents=input_content
                    )
                    st.success("Tayyorlangan javob:")
                    st.write(response.text)
                except Exception as e:
                    st.error(f"Xatolik: {e}")
            else:
                st.error("Iltimos, ma'lumot kiriting!")

with tab2:
    st.subheader("60 ta mahalla bo'yicha tahlil")
    df = pd.DataFrame({
        "Mahalla nomi": [f"{i}-sonli mahalla" for i in range(1, 61)],
        "Kelgan": [0] * 60,
        "Yopildi": [0] * 60
    })
    st.dataframe(df, use_container_width=True)

with tab3:
    st.subheader("🔄 Qayta murojaatlar nazorati")
    st.info("Tizim qayta murojaatlarni aniqlashga tayyor.")
