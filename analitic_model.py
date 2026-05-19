import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report

# ==========================================
# 1. ГЕНЕРАЦИЯ ДАННЫХ И ФОРМИРОВАНИЕ ВЫБОРКИ
# ==========================================
np.random.seed(42)
days = 300

# Симулируем цену закрытия акции (случайное блуждание с трендом)
start_price = 100.0
price_changes = np.random.normal(loc=0.05, scale=1.5, size=days)
prices = start_price + np.cumsum(price_changes)

df = pd.DataFrame({"Close": prices})

# Расчет технических индикаторов (Признаки / Features)
df["MA_5"] = df["Close"].rolling(window=5).mean()  # Краткосрочная скользящая средняя
df["MA_15"] = df["Close"].rolling(window=15).mean()  # Среднесрочная скользящая средняя
df["Vol_5"] = df["Close"].rolling(window=5).std()  # Волатильность за 5 дней

# Индикатор RSI (упрощенная версия)
delta = df["Close"].diff()
gain = delta.where(delta > 0, 0)
loss = -delta.where(delta < 0, 0)
avg_gain = gain.rolling(window=14).mean()
avg_loss = loss.rolling(window=14).mean()
rs = avg_gain / (avg_loss + 1e-9)
df["RSI"] = 100 - (100 / (1 + rs))

# Целевая переменная (Target): 1, если завтра цена выше, чем сегодня, иначе 0
df["Target"] = (df["Close"].shift(-1) > df["Close"]).astype(int)

# Удаляем строки с пустыми значениями из-за скользящих окон
df.dropna(inplace=True)

# Разделение на признаки (X) и целевой класс (y)
X = df[["MA_5", "MA_15", "Vol_5", "RSI"]]
y = df["Target"]

# Деление выборки на обучающую (80%) и тестовую (20%)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, shuffle=False
)

# ==========================================
# 2. РЕАЛИЗАЦИЯ И ОБУЧЕНИЕ МЕТОДА ИАД
# ==========================================
# Инициализируем модель Случайного Леса
model = RandomForestClassifier(n_estimators=100, max_depth=5, random_state=42)

# Обучаем модель на исторических данных
model.fit(X_train, y_train)

# Прогнозирование на тестовой выборке
y_pred = model.predict(X_test)

# ==========================================
# 3. АНАЛИЗ РЕЗУЛЬТАТОВ
# ==========================================
accuracy = accuracy_score(y_test, y_pred)
print(f"Точность прогнозирования (Accuracy): {accuracy:.2%}\n")
print("Детальный отчет по метрикам:")
print(classification_report(y_test, y_pred, target_names=["Падение (0)", "Рост (1)"]))

# Вывод значимости признаков
importances = model.feature_importances_
print("Значимость признаков для модели:")
for name, importance in zip(X.columns, importances):
    print(f" - {name}: {importance:.2%}")
