import sqlite3

# Создание соединения с БД в памяти
conn = sqlite3.connect(":memory:")
cursor = conn.cursor()

# Создание таблиц
cursor.execute("""
CREATE TABLE Assets (
    asset_id INTEGER PRIMARY KEY AUTOINCREMENT,
    ticker TEXT NOT NULL UNIQUE,
    name TEXT NOT NULL
)""")

cursor.execute("""
CREATE TABLE Quotes (
    quote_id INTEGER PRIMARY KEY AUTOINCREMENT,
    asset_id INTEGER,
    timestamp DATETIME NOT NULL,
    close_price REAL NOT NULL,
    volume INTEGER,
    FOREIGN KEY(asset_id) REFERENCES Assets(asset_id)
)""")

cursor.execute("""
CREATE TABLE DecisionLog (
    decision_id INTEGER PRIMARY KEY AUTOINCREMENT,
    asset_id INTEGER,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    predicted_signal TEXT,
    situation_class TEXT,
    recommended_action TEXT,
    FOREIGN KEY(asset_id) REFERENCES Assets(asset_id)
)""")

# Наполнение тестовыми данными
cursor.execute("INSERT INTO Assets (ticker, name) VALUES ('SBER', 'Сбербанк')")
cursor.execute(
    "INSERT INTO Quotes (asset_id, timestamp, close_price, volume) VALUES (1, '2026-05-18 10:00:00', 285.50, 15000)"
)
cursor.execute(
    "INSERT INTO Quotes (asset_id, timestamp, close_price, volume) VALUES (1, '2026-05-18 11:00:00', 287.20, 18000)"
)
conn.commit()

print("База данных СППР успешно инициализирована.")


import numpy as np
import pandas as pd
import time
from datetime import datetime


class FinancialDSS:
    def __init__(self, ticker):
        self.ticker = ticker
        print(f"=== СППР 'АЛГО-ТРЕЙД' ЗАПУЩЕНА ДЛЯ АКТИВА: {self.ticker} ===")

    def get_realtime_market_data(self):
        """Эмуляция оболочки: получение текущего состояния рынка"""
        np.random.seed(int(time.time()))
        current_price = round(250.0 + np.random.uniform(-5.0, 5.0), 2)
        rsi = round(np.random.uniform(20, 80), 1)
        volatility = round(np.random.uniform(0.5, 4.5), 2)
        return {"Цена": current_price, "RSI": rsi, "Волатильность": volatility}

    # ИИ Функционал А: Прогнозирование параметров
    def ai_predict_trend(self, data):
        """Прогноз направления движения на основе индикатора RSI"""
        if data["RSI"] < 35:
            return "Цена вырастет (Технический отскок из зоны перепроданности)"
        elif data["RSI"] > 65:
            return "Цена упадет (Коррекция из зоны перекупленности)"
        else:
            return "Стабильное движение (Цена останется в текущем коридоре)"

    # ИИ Функционал Б: Классификация ситуации
    def ai_classify_situation(self, data):
        """Классификация рыночного состояния по уровню волатильности"""
        if data["Волатильность"] > 3.0:
            return "ИМПУЛЬСНЫЙ ТРЕНД (Высокий риск, сильные движения)"
        elif data["Волатильность"] < 1.5:
            return "НИЗКОВОЛАТИЛЬНЫЙ ФЛЭТ (Затишье перед распределением)"
        else:
            return "НОРМАЛЬНЫЙ РЫНОК (Стандартный торговый режим)"

    # ИИ Функционал В: Создание сценария действий
    def ai_create_scenario(self, trend, situation, data):
        """Генерация комплексного инвестиционного сценария на основе ИИ-анализа"""
        scenario = []
        if "вырастет" in trend and "ФЛЭТ" in situation:
            scenario.append(
                "Сценарий А: Накопление позиции. Покупка частями со стоп-лоссом ниже границы флэта."
            )
        elif "упадет" in trend and "ИМПУЛЬСНЫЙ" in situation:
            scenario.append(
                "Сценарий Б: Экстренный хедж. Закрытие лонгов, покупка защитных путов."
            )
        else:
            scenario.append(
                "Сценарий В: Ожидание. Удерживать текущий портфель без активных спекуляций."
            )

        scenario.append(f"Расчетный Stop-Loss: {round(data['Цена'] * 0.98, 2)} руб.")
        scenario.append(f"Расчетный Take-Profit: {round(data['Цена'] * 1.05, 2)} руб.")
        return scenario

    def run_dashboard(self):
        """Визуализация работы интерфейса СППР в реальном времени"""
        market_data = self.get_realtime_market_data()

        # Запуск ИИ вычислений
        trend_pred = self.ai_predict_trend(market_data)
        situation_class = self.ai_classify_situation(market_data)
        action_scenario = self.ai_create_scenario(
            trend_pred, situation_class, market_data
        )

        # Отражение основных данных в интерфейсе оболочки
        print("\n" + "=" * 50)
        print(f"МОНИТОР ДАННЫХ | Время: {datetime.now().strftime('%H:%M:%S')}")
        print("-" * 50)
        print(f" Текущая котировка: {market_data['Цена']} руб.")
        print(f" Индикатор RSI:     {market_data['RSI']}")
        print(f" Волатильность:     {market_data['Волатильность']}%")
        print("-" * 50)
        print(f" [ИИ] КЛАССИФИКАЦИЯ СИТУАЦИИ: {situation_class}")
        print(f" [ИИ] ПРОГНОЗ ПАРАМЕТРОВ:     {trend_pred}")
        print("-" * 50)
        print(" [ИИ] РЕКОМЕНДУЕМЫЙ СЦЕНАРИЙ ДЕЙСТВИЙ:")
        for step in action_scenario:
            print(f"   -> {step}")
        print("=" * 50 + "\n")


# Запуск демонстрационного цикла СППР в реальном времени
dss = FinancialDSS("SBER")
# Симуляция 2-х тиков обновления данных в панели управления
for _ in range(2):
    dss.run_dashboard()
    time.sleep(1)  # Задержка между обновлениями экрана
