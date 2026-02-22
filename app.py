import streamlit as st
import requests
import json

# Читаем ключ из секретов
API_KEY = st.secrets["GEN_API_KEY"]
# Endpoint для ChatGPT-3 через gen-api.ru
API_URL = "https://api.gen-api.ru/api/v1/networks/chat-gpt-3"

def generate_email(topic, product, audience, tone):
    """
    Отправляет запрос к gen-api.ru и возвращает сгенерированное письмо.
    """
    # Формируем сообщения для ChatGPT
    messages = [
        {
            "role": "system",
            "content": "Ты — профессиональный копирайтер, который помогает создавать эффективные email-рассылки."
        },
        {
            "role": "user",
            "content": f"""
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
        }
    ]
    
    # Параметры запроса
    payload = {
        "messages": messages,
        "is_sync": True,          # синхронный режим – ответ сразу
        "temperature": 0.7,
        "max_tokens": 2000,
    }
    
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Authorization": f"Bearer {API_KEY}"
    }
    
    # Отправляем POST-запрос
    response = requests.post(API_URL, json=payload, headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        # Извлекаем текст из ответа согласно структуре gen-api.ru
        if "response" in data and len(data["response"]) > 0:
            # Берём первый вариант генерации (индекс 0)
            first_response = data["response"][0]
            if "message" in first_response and "content" in first_response["message"]:
                return first_response["message"]["content"]
            else:
                raise Exception("Не удалось найти content в ответе: " + str(first_response))
        else:
            raise Exception("Нет поля 'response' в ответе: " + str(data))
    else:
        raise Exception(f"HTTP {response.status_code}: {response.text}")

# Интерфейс Streamlit
st.set_page_config(page_title="AI Email Assistant (ChatGPT via gen-api.ru)", page_icon="✉️")
st.title("✉️ AI-помощник для email-рассылок")
st.write("Заполните параметры, и нейросеть напишет письмо за вас.")

with st.form("email_form"):
    topic = st.text_input("Тема письма", "Анонс новой коллекции")
    product = st.text_area("Описание продукта/акции", "Мы запустили линейку экологичных кроссовок из переработанных материалов.")
    audience = st.text_input("Целевая аудитория", "Молодёжь 20–35 лет, увлекающаяся спортом и экологией")
    tone = st.selectbox("Тон письма", ["дружеский", "формальный", "убеждающий"])
    submitted = st.form_submit_button("Сгенерировать")

if submitted:
    with st.spinner("Нейросеть пишет письмо..."):
        try:
            email = generate_email(topic, product, audience, tone)
            st.subheader("Готовое письмо:")
            st.text_area("Результат", email, height=400)
            st.button("📋 Копировать", help="Выделите текст и скопируйте вручную")
        except Exception as e:
            st.error(f"Ошибка: {e}")
