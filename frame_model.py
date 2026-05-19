class CurrencyFrame:
    """Базовый фрейм валюты (прототип)"""

    def __init__(self, name, current_rate, prev_rate):
        self.name = name
        self.current_rate = current_rate
        self.prev_rate = prev_rate
        self.trend = self.calculate_trend()

    def calculate_trend(self):
        diff = ((self.current_rate - self.prev_rate) / self.prev_rate) * 100
        return round(diff, 2)


class ExpertSystem:
    """Фрейм-инференс (логика принятия решений)"""

    @staticmethod
    def analyze(currency):
        print(f"--- Анализ {currency.name} ---")
        print(f"Текущий курс: {currency.current_rate} | Изменение: {currency.trend}%")

        # Правила вывода (слоты с присоединенными процедурами)
        if currency.trend > 1.5:
            return "РЕКОМЕНДАЦИЯ: Продавать (Резкий рост)"
        elif currency.trend < -1.5:
            return "РЕКОМЕНДАЦИЯ: Покупать (Сильное падение)"
        else:
            return "РЕКОМЕНДАЦИЯ: Удерживать (Стабильность)"


# RAD-разработка: Быстрое создание экземпляров (фреймов-экземпляров)
usd = CurrencyFrame("USD/RUB", 92.50, 91.00)
eur = CurrencyFrame("EUR/RUB", 100.10, 100.05)

# Работа экспертной системы
print(ExpertSystem.analyze(usd))
print(ExpertSystem.analyze(eur))
