import streamlit as st
import requests
import json

# Читаем данные из секретов
IAM_TOKEN = st.secrets["YC_IAM_TOKEN"]
FOLDER_ID = st.secrets["YC_FOLDER_ID"]

# URL для YandexGPT API
YANDEX_GPT_URL = "https://llm.api.cloud.yandex.net/foundationModels/v1/completion"

def generate_yandex_text(prompt, temperature=0.7, max_tokens=2000):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {IAM_TOKEN}",
        "x-folder-id": FOLDER_ID
    }
    
    data = {
        "modelUri": f"gpt://{FOLDER_ID}/yandexgpt-lite",  # или yandexgpt для лучшего качества
        "completionOptions": {
            "stream": False,
            "temperature": temperature,
            "maxTokens": str(max_tokens)
        },
        "messages": [
            {
                "role": "system",
                "text": "Ты — профессиональный копирайтер, который помогает создавать эффективные email-рассылки."
            },
            {
                "role": "user",
                "text": prompt
            }
        ]
    }
    
    response = requests.post(YANDEX_GPT_URL, headers=headers, json=data)
    
    if response.status_code == 200:
        result = response.json()
        # Извлекаем текст ответа
        return result['result']['alternatives'][0]['message']['text']
    else:
        raise Exception(f"Ошибка API: {response.status_code} - {response.text}")

# Дальше код Streamlit аналогичен первому варианту
