import streamlit as st
import openai

openai.api_key = st.secrets["OPENAI_API_KEY"]

st.title("✉️ AI-помощник для email-рассылок")
st.write("Заполните параметры, и нейросеть напишет письмо за вас.")

topic = st.text_input("Тема письма", "Анонс новой коллекции")
product = st.text_area("Описание продукта/акции", "Мы запустили линейку экологичных кроссовок из переработанных материалов.")
audience = st.text_input("Целевая аудитория", "Молодёжь 20–35 лет, увлекающаяся спортом и экологией")
tone = st.selectbox("Тон письма", ["дружеский", "формальный", "убеждающий"])

if st.button("Сгенерировать"):
    with st.spinner("Нейросеть пишет письмо..."):
        prompt = f"""
        Напиши email-письмо для маркетинговой рассылки.
        Тема: {topic}
        Продукт: {product}
        Аудитория: {audience}
        Тон: {tone}
        
        Письмо должно содержать:
        - заголовок;
        - приветствие;
        - основную часть с описанием выгоды;
        - призыв к действию;
        - прощание.
        """
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7
        )
        email = response.choices[0].message.content
        st.subheader("Готовое письмо:")
        st.text_area("Результат", email, height=400)
        st.button("Копировать", on_click=lambda: st.write("Скопировано (здесь нужен JavaScript)"))  # упрощённо
