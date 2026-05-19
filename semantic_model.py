import streamlit as st  # RAD-инструмент для UI


# 1. БАЗА ЗНАНИЙ (Семантические правила)
def get_recommendation(change_pct):
    if change_pct > 5:
        return (
            "Критический рост",
            "Резкое обесценивание национальной валюты. Рекомендуется фиксация прибыли (продажа).",
        )
    elif 1 < change_pct <= 5:
        return (
            "Умеренный рост",
            "Тренд на повышение. Подходящее время для постепенного выхода из валютных позиций.",
        )
    elif -1 <= change_pct <= 1:
        return "Стабильность", "Рынок находится в равновесии. Операции не требуются."
    elif -5 <= change_pct < -1:
        return (
            "Умеренное падение",
            "Валюта дешевеет. Благоприятный момент для начала формирования накоплений.",
        )
    else:
        return (
            "Глубокая коррекция",
            "Курс минимален. Рекомендуется активная покупка (Long).",
        )


# 2. ИНТЕРФЕЙС (RAD-подход)
st.title("Экспертная система: Анализ валютных курсов")
st.subheader("Семантический вывод на основе динамики")

col1, col2 = st.columns(2)
with col1:
    prev_price = st.number_input("Курс на вчера", value=90.0)
with col2:
    curr_price = st.number_input("Курс на сегодня", value=92.5)

# 3. РАБОТА МЕХАНИЗМА ВЫВОДА
if st.button("Провести экспертизу"):
    change = ((curr_price - prev_price) / prev_price) * 100
    status, advice = get_recommendation(change)

    st.divider()
    st.metric("Изменение курса", f"{curr_price} RUB", f"{change:.2f}%")

    st.info(f"**Вердикт системы:** {status}")
    st.write(advice)
