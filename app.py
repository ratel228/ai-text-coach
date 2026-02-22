import streamlit as st
import openai
import json
import os

openai.api_key = st.secrets["OPENAI_API_KEY"]  # безопасно храним ключ

def analyze_text(text):
    prompt = f"Ты редактор. Оцени текст по шкале от 0 до 10 по параметрам: стиль, структура, эмоции. Дай совет. Текст: {text}"
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3
    )
    return response.choices[0].message.content

st.title("🧠 AI-тренер текстов")
st.write("Вставьте текст, и я дам обратную связь как опытный редактор.")

text = st.text_area("Ваш текст", height=150)

if st.button("Проанализировать"):
    if text:
        with st.spinner("Думаю..."):
            result = analyze_text(text)
        st.success("Готово!")
        st.write(result)
    else:
        st.warning("Сначала введите текст.")
