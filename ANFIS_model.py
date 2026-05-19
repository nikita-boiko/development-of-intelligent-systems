import numpy as np

# 1. Данные для обучения (Ставка, Нефть, Инфляция -> Курс)
X = np.array([[16.0, 85.0, 9.0], [5.0, 40.0, 3.0], [10.0, 60.0, 5.0]])
y = np.array([85.5, 105.2, 92.0])

# 2. Параметры системы (обучаемые центры функций принадлежности)
centers = np.array([[5.0, 15.0], [40.0, 90.0], [2.0, 10.0]])
weights = np.random.randn(8)  # Веса 8 правил (2^3)
lr = 0.001  # Скорость обучения


def get_output(inputs):
    # Фаззификация (Гаусс)
    m = np.exp(-((inputs.reshape(3, 1) - centers) ** 2) / 25.0)

    # Формирование 8 правил (степень срабатывания)
    rules = []
    for r1 in [0, 1]:
        for r2 in [0, 1]:
            for r3 in [0, 1]:
                rules.append(m[0, r1] * m[1, r2] * m[2, r3])
    rules = np.array(rules)

    # Дефаззификация
    return np.dot(rules, weights) / (np.sum(rules) + 1e-9), rules


# 3. Мини-цикл обучения (Нейро-часть)
for _ in range(500):
    for i in range(len(X)):
        pred, r = get_output(X[i])
        error = pred - y[i]
        # Корректировка весов правил (градиентный спуск)
        weights -= lr * error * r

# Тест
test_input = np.array([16.0, 85.0, 9.0])
res, _ = get_output(test_input)
print(f"Прогноз курса (Neuro-Fuzzy): {res:.2f}")
