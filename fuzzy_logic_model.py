import numpy as np
import skfuzzy as fuzzy
from skfuzzy import control as ctrl

# 1. Определение осей (Universe)
rate = ctrl.Antecedent(np.arange(0, 21, 1), "rate")  # Ставка ЦБ
oil = ctrl.Antecedent(np.arange(20, 121, 1), "oil")  # Цена на нефть
currency = ctrl.Consequent(np.arange(-5, 6, 1), "currency")  # Изменение курса

# 2. Функции принадлежности (автоматическая генерация для простоты)
rate.automf(3, names=["low", "medium", "high"])
oil.automf(3, names=["low", "stable", "high"])

currency["strengthening"] = fuzzy.trimf(currency.universe, [-5, -5, 0])
currency["stable"] = fuzzy.trimf(currency.universe, [-2, 0, 2])
currency["weakening"] = fuzzy.trimf(currency.universe, [0, 5, 5])

# 3. База правил
rule1 = ctrl.Rule(oil["high"] | rate["high"], currency["strengthening"])
rule2 = ctrl.Rule(oil["low"], currency["weakening"])
rule3 = ctrl.Rule(rate["medium"] & oil["stable"], currency["stable"])

# 4. Система вывода
predict_ctrl = ctrl.ControlSystem([rule1, rule2, rule3])
prediction = ctrl.ControlSystemSimulation(predict_ctrl)

# Ввод данных
prediction.input["rate"] = 15  # Высокая ставка
prediction.input["oil"] = 90  # Высокая нефть

# Вычисление
prediction.compute()

print(f"Прогноз изменения курса: {prediction.output['currency']:.2f}%")
