import streamlit as st
import google.generativeai as genai
from PIL import Image
from PyPDF2 import PdfReader
import io

st.set_page_config(page_title="Mahijro AI", page_icon="🏛")

# ✅ API KEY (hozircha to‘g‘ridan qo‘y)
genai.configure(api_key="SENING_YANGI_API_KEY")

# ✅ TO‘G‘RI MODEL
model = genai.GenerativeModel("gemini-1.5-flash-latest")
# agar ishlamasa:
# model = genai.GenerativeModel("gemini-2.0-flash")

# 2. Ma'lumotlar
positions = [
    "1. Mahallalar uyushmasi boshlig'i",
    "2. IIB boshlig'i",
    "3. 'Inson' markazi direktori",
    "4. Yoshlar agentligi boshlig'i",
    "5. Soliq boshlig'i",
    "6. Oila va xotin-qizlar boshlig'i",
    "7. Mahallabay agentligi boshlig'i"
]

mfy_list = ["Abdujalilbob","Alimbuva","Amir Temur","Asil","Axilobod","Ahmad Yassaviy","Baliqchi","Bog'zor","Bog'ishamol","Bodomzor","Bo'ston","Gulbog'","Daligazar","Dehqonobod","Zarafshon","Ilg'or","Istiqlol","Istiqlolning 5-yilligi","Katta chinor","Keng kechik","Qahramon","Quyoshli","Qurilish","M.M.Xorazmiy","Madaniyat","Mevazor","Navbahor","Navqiron","Nazarbek","Nayman","Namuna","Nurafshon","Nurobod","Obod","Obod to'qimachi","Obod turmush","Olmazor","Ramadon","Saxovat","Sortepa","Tariq-teshar","Tarnov","Tokzor","To'qimachi","Turkiston","Turopobod","O'ratepa","O'rikzor","O'rta","O'rtaovul","Fayz","Farobiy","Harakat","Xo'jamozor","Chinor","Shodlik","Erkin","Eski qala","Eshonguzar","Yangi bo'zsuv"]

# UI
st.title("🏛 Mahijro AI: Zangiota tumani")

rahbar = st.selectbox("Mas'ul rahbar:", positions)
mfy = st.selectbox("Mahalla:", mfy_list)

murojaat = st.file_uploader("Murojaatni yuklang:", type=['png', 'jpg', 'pdf'])
dalolatnoma = st.file_uploader("Dalolatnoma (Ixtiyoriy):", type=['png', 'jpg', 'pdf'])

if st.button("🚀 Javobni tayyorlash"):
    if murojaat:
        with st.spinner("Tahlil qilinmoqda..."):
            try:
                prompt = f"Siz {rahbar}siz. {mfy} mahallasi uchun rasmiy javob yozing. Lotin alifbosida."
                content = [prompt]

                # PDF
                if murojaat.type == "application/pdf":
                    reader = PdfReader(io.BytesIO(murojaat.read()))
                    text = ""
                    for p in reader.pages:
                        if p.extract_text():
                            text += p.extract_text()
                    content.append("Arizada shunday yozilgan: " + text)

                # RASM
                else:
                    image = Image.open(murojaat)
                    content.append(image)

                # Qo‘shimcha fayl
                if dalolatnoma:
                    image2 = Image.open(dalolatnoma)
                    content.append(image2)

                res = model.generate_content(content)

                st.success("Bajarildi!")
                st.write(res.text)

            except Exception as e:
                st.error(f"Xatolik: {e}")
    else:
        st.warning("Murojaat yuklang!")
