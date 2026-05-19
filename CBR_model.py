import pandas as pd
from sklearn.neighbors import NearestNeighbors
import numpy as np

# 1. База прецедентов (набор исторических данных)
# Признаки: [Инфляция %, Цена на нефть, Ставка ЦБ %]
# Исход: % изменения курса валюты
data = {
    "inflation": [2.1, 8.5, 4.0, 12.0, 3.5, 9.0],
    "oil_price": [70, 40, 80, 30, 75, 45],
    "interest_rate": [5.0, 15.0, 7.5, 20.0, 6.0, 17.0],
    "currency_change": [0.1, 2.5, -0.5, 5.0, 0.2, 3.0],  # Целевой показатель
}

df = pd.DataFrame(data)


# 2. Движок CBR (Используем метод ближайших соседей)
class CurrencyExpertSystem:
    def __init__(self, cases):
        self.cases = cases
        self.features = cases[["inflation", "oil_price", "interest_rate"]]
        self.model = NearestNeighbors(n_neighbors=1, algorithm="auto").fit(
            self.features
        )

    def solve(self, current_situation):
        # Поиск самого похожего прецедента
        dist, index = self.model.kneighbors([current_situation])
        best_match = self.cases.iloc[index[0][0]]

        return {
            "predicted_change": best_match["currency_change"],
            "similarity_score": 1 / (1 + dist[0][0]),
            "matched_case": best_match.to_dict(),
        }


# 3. Работа с системой
expert = CurrencyExpertSystem(df)

# Текущая ситуация на рынке
current_market = [4.2, 78, 7.0]  # Инфляция 4.2, Нефть 78, Ставка 7.0
result = expert.solve(current_market)

print(f"Прогноз изменения курса: {result['predicted_change']}%")
print(f"Сходство с прецедентом: {result['similarity_score']:.2f}")
print(f"Наиболее похожий случай из базы: {result['matched_case']}")
