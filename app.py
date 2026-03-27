if st.button("🚀 Javobni tayyorlash"):
    if murojaat:
        with st.spinner("AI tahlil qilmoqda..."):
            try:
                # Promptni shakllantirish
                prompt_text = f"Siz {rahbar}siz. {mfy} mahallasi uchun rasmiy javob yozing. Faqat lotin alifbosida."
                
                # Kontentni yig'ish
                final_content = [prompt_text]
                
                if murojaat.type == "application/pdf":
                    reader = PdfReader(io.BytesIO(murojaat.read()))
                    pdf_text = "".join([p.extract_text() for p in reader.pages])
                    if pdf_text.strip():
                        final_content.append(f"Murojaat matni: {pdf_text}")
                    else:
                        st.warning("PDF ichidan matn topilmadi, rasm sifatida tahlil qilinmoqda.")
                        # PDFdan rasm sifatida foydalanish murakkabroq, shuning uchun matn bo'lmasa ogohlantiramiz
                else:
                    final_content.append(Image.open(murojaat))

                # Dalolatnoma bo'lsa qo'shish
                if dalolatnoma:
                    final_content.append(Image.open(dalolatnoma))

                # AIga yuborish
                res = model.generate_content(final_content)
                st.success("Tayyor!")
                st.write(res.text)
            except Exception as e:
                st.error(f"Generatsiya jarayonida xatolik: {e}")
