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
    st.warning("API kalit topilmadi. Secrets bo'limini tekshiring.")
    st.stop()

client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])

tab1, tab2, tab3 = st.tabs(["✍️ Murojaat yuklash", "📊 Mahallalar hisoboti", "🔄 Qayta murojaatlar"])

with tab1:
    st.subheader("Murojaatni yuklang (Rasm yoki PDF)")
    
    uploaded_file = st.file_uploader("Faylni tanlang", type=['png', 'jpg', 'jpeg', 'pdf'])
    murojaat_text = st.text_area("Qo'shimcha izoh:", height=100)
    
    if st.button("Javob xati tayyorlash"):
        if uploaded_file or murojaat_text:
            with st.spinner("Tahlil qilinmoqda..."):
                input_content = []
                # Ko'rsatma (Prompt)
                input_content.append("Siz davlat idorasi xodimisiz. Murojaatni O'zbekiston qonunchiligi asosida o'rganib, rasmiy javob xati tayyorlang.")

                if murojaat_text:
                    input_content.append(f"Qo'shimcha matn: {murojaat_text}")
                
                if uploaded_file:
                    if uploaded_file.type == "application/pdf":
                        try:
                            pdf_reader = PdfReader(uploaded_file)
                            text = ""
                            for page in pdf_reader.pages:
                                text += page.extract_text()
                            input_content.append(f"PDF matni: {text}")
                        except:
                            st.error("PDF-ni o'qib bo'lmadi.")
                    else:
                        img = Image.open(uploaded_file)
                        input_content.append(img)

                try:
                    # AI-ga yuborish
                    response = client.models.generate_content(
                        model="gemini-2.0-flash",
                        contents=input_content
                    )
                    st.success("Tayyorlangan javob:")
                    st.write(response.text)
                except Exception as e:
                    st.error(f"AI bilan aloqa uzildi. API kalitni tekshiring.")
        else:
            st.error("Iltimos, fayl yuklang!")

with tab2:
    st.subheader("60 ta mahalla bo'yicha tahlil")
    # Zangiota tumani mahalla tizimi uchun namunaviy jadval
    df = pd.DataFrame({
        "Mahalla": [f"Mahalla {i}" for i in range(1, 61)],
        "Holat": ["Jarayonda"] * 60
    })
    st.dataframe(df, use_container_width=True)
