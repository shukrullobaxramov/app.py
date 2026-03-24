import streamlit as st
from google import genai
import pandas as pd

# Илованинг сарлавҳаси
st.set_page_config(page_title="Mahijro AI", page_icon="🏛")
st.title("🏛 Mahijro AI")
st.markdown("##### Давлат хизматчилари учун мурожаатларга тезкор ва қонуний жавоб тайёрлаш тизими")

# API калитни текшириш
if "GEMINI_API_KEY" not in st.secrets:
    st.warning("Тизим созланмоқда. Илтимос, API калитни Secrets бўлимига киритинг.")
    st.stop()

client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])

# Кириш пароли
CORRECT_PASSWORD = "123"

if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

if not st.session_state["authenticated"]:
    password = st.text_input("Кириш паролини ёзинг:", type="password")
    if st.button("Тизимга кириш"):
        if password == CORRECT_PASSWORD:
            st.session_state["authenticated"] = True
            st.rerun()
        else:
            st.error("Парол нотўғри!")
    st.stop()

# Асосий меню
tab1, tab2, tab3 = st.tabs(["✍️ Жавоб ёзиш", "📊 Маҳаллалар ҳисоботи", "🔄 Қайта мурожаатлар"])

with tab1:
    murojaat = st.text_area("Мурожаат матнини киритинг:", height=200)
    if st.button("Жавоб хати тайёрлаш"):
        if murojaat:
            with st.spinner("AI таҳлил қилмоқда..."):
                response = client.models.generate_content(
                    model="gemini-2.0-flash",
                    contents=f"Қуйидаги мурожаатга Ўзбекистон қонунчилиги асосида расмий жавоб хати ёзиб бер: {murojaat}"
                )
                st.subheader("Тайёрланган жавоб:")
                st.write(response.text)
        else:
            st.error("Илтимос, мурожаат матнини киритинг.")

with tab2:
    st.subheader("60 та маҳалла бўйича мурожаатлар статистикаси")
    # Намунавий маълумотлар
    data = {"Маҳалла": [f"Маҳалла {i}" for i in range(1, 61)], 
            "Мурожаатлар сони": [0] * 60,
            "Ижро этилган": [0] * 60}
    df = pd.DataFrame(data)
    st.dataframe(df, use_container_width=True)

with tab3:
    st.subheader("🔄 Қайта келган мурожаатлар назорати")
    st.info("Бу ерда қайта келган мурожаатлар автоматик таҳлил қилинади.")

st.sidebar.markdown("---")
st.sidebar.write("© 2026 Mahijro AI")
