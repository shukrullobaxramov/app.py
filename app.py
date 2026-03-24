import streamlit as st
from google import genai
from PIL import Image
import pandas as pd

# Sahifa sozlamalari
st.set_page_config(page_title="Mahijro AI", page_icon="🏛")
st.title("🏛 Mahijro AI")
st.markdown("##### Murojaatlarga tezkor va qonuniy javob tayyorlash tizimi")

# API kalitni tekshirish
if "GEMINI_API_KEY" not in st.secrets:
    st.warning("Tizim sozlanmoqda. API kalitni Secrets bo'limiga kiriting.")
    st.stop()

client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])

# Bo'limlar
tab1, tab2, tab3 = st.tabs(["✍️ Murojaat yuklash", "📊 Mahallalar hisoboti", "🔄 Qayta murojaatlar"])

with tab1:
    st.subheader("Murojaatni matn yoki rasm ko'rinishida kiriting")
    
    # Fayl yuklash
    uploaded_file = st.file_uploader("Murojaat rasmini yuklang", type=['png', 'jpg', 'jpeg'])
    
    murojaat_text = st.text_area("Yoki murojaat matnini bu yerga yozing:", height=150)
    
    if st.button("Javob xati tayyorlash"):
        with st.spinner("AI tahlil qilmoqda..."):
            input_content = []
            
            # AI uchun asosiy ko'rsatma (tizim xatosi bo'lmasligi uchun sodda tilda)
            prompt = "Siz davlat idorasi xodimisiz. Quyidagi murojaatni O'zbekiston qonunchiligi asosida o'rganib chiqib, rasmiy javob xati loyihasini o'zbek tilida tayyorlab bering:"
            input_content.append(prompt)

            if murojaat_text:
                input_content.append(murojaat_text)
            
            if uploaded_file:
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
                    st.error(f"Xatolik yuz berdi: {e}")
            else:
                st.error("Iltimos, matn yozing yoki rasm yuklang!")

with tab2:
    st.subheader("60 ta mahalla bo'yicha tahlil")
    # Mahalla statistikasi (Namuna)
    df = pd.DataFrame({
        "Mahalla nomi": [f"{i}-sonli mahalla" for i in range(1, 61)],
        "Murojaatlar": [0] * 60,
        "Bajarildi": [0] * 60
    })
    st.dataframe(df, use_container_width=True)

with tab3:
    st.subheader("🔄 Qayta murojaatlar nazorati")
    st.info("Tizim avvalgi murojaatlarni tahlil qilishga tayyor.")
