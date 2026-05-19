from sklearn.tree import DecisionTreeClassifier, plot_tree
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.datasets import make_classification

# Создание датасета (330 примеров)
X, y = make_classification(n_samples=330, n_features=4, random_state=42)
X_train, X_test = X[:300], X[300:]
y_train, y_test = y[:300], y[300:]

# Построение модели
model = DecisionTreeClassifier(max_depth=3)
model.fit(X_train, y_train)

# Оценка
error = (1 - accuracy_score(y_test, model.predict(X_test))) * 100
print(f"Процент ошибки: {error:.2f}%")
