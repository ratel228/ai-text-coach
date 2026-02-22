import streamlit as st
from openai import OpenAI

# Настраиваем подключение к ChatGPT
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

def analyze_text(text):
    # Это функция, которая отправляет текст в ChatGPT и получает ответ
    prompt = f"""Ты опытный редактор и тренер по текстам. Оцени текст по трём параметрам:
1. Соответствие тону бренда (дружелюбный эксперт) – от 0 до 10.
2. Структура (заголовок, проблема, решение, призыв) – от 0 до 10.
3. Эмоциональный окрас (например, "сухо", "восторженно", "нейтрально").
И дай один главный совет по улучшению.

Текст: {text}

Ответ верни в формате JSON, например:
{{"tone_score": 8, "structure_score": 6, "emotion": "сухо", "advice": "добавьте конкретные примеры"}}
"""

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",  # используем не самую дорогую модель
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3
    )
    return response.choices[0].message.content

# Здесь начинается веб-интерфейс
st.set_page_config(page_title="AI-тренер текстов")
st.title("🧠 AI-тренер текстов")
st.write("Вставьте текст, и я дам обратную связь как опытный редактор.")

# Создаём поле для ввода текста
user_text = st.text_area("Ваш текст", height=150)

# Кнопка для запуска анализа
if st.button("Проанализировать"):
    if user_text:
        with st.spinner("Думаю..."):
            result = analyze_text(user_text)
        st.success("Готово!")
        # Пытаемся распарсить JSON, если получится — выводим красиво, иначе просто текст
        try:
            import json
            data = json.loads(result)
            st.metric("Соответствие ToV", f"{data['tone_score']}/10")
            st.metric("Структура", f"{data['structure_score']}/10")
            st.write("Эмоции:", data['emotion'])
            st.info(f"💡 Совет: {data['advice']}")
        except:
            st.write(result)
    else:
        st.warning("Сначала введите текст.")
