import numpy as np
from sklearn.neural_network import MLPRegressor
import matplotlib.pyplot as plt


# --- 1. Окружение склада ---
class WarehouseEnv:
    def __init__(self):
        self.max_capacity = 50
        self.state = 20.0  # Начальный запас
        self.c_store = 1.0
        self.c_pen = 5.0
        self.c_order = 2.0

    def reset(self):
        self.state = 20.0
        return np.array([self.state], dtype=np.float32)

    def step(self, action):
        order = max(0.0, float(action))

        # Случайный спрос
        demand = np.random.normal(loc=10.0, scale=3.0)
        demand = max(0.0, demand)

        # Запас после заказа, но до спроса
        self.state = min(self.max_capacity, self.state + order)

        # Запас на конец дня после спроса
        self.state -= demand

        # Расчет подкрепления
        reward = 0.0
        if self.state >= 0:
            reward -= self.c_store * self.state
        else:
            reward -= self.c_pen * abs(self.state)

        if order > 0:
            reward -= self.c_order

        self.state = max(-20.0, self.state)
        return np.array([self.state], dtype=np.float32), reward


# --- 2. Инициализация моделей scikit-learn ---
# Используем MLPRegressor с SGD/Adam для онлайн-обучения (partial_fit)
actor = MLPRegressor(
    hidden_layer_sizes=(32,), activation="relu", solver="adam", learning_rate_init=0.01
)
critic = MLPRegressor(
    hidden_layer_sizes=(32,), activation="relu", solver="adam", learning_rate_init=0.02
)

# В sklearn нужно сделать "холостой" partial_fit, чтобы инициализировать веса под размерность входа
dummy_state = np.array([[20.0]])
dummy_target = np.array([0.0])
actor.partial_fit(dummy_state, dummy_target)
critic.partial_fit(dummy_state, dummy_target)


# --- 3. Обучение ---
env = WarehouseEnv()
gamma = 0.95
rewards_history = []
epochs = 200
steps_per_epoch = 30

print("Запуск обучения адаптивного критика (scikit-learn)...")

for epoch in range(epochs):
    state = env.reset()
    epoch_reward = 0

    for step in range(steps_per_epoch):
        # Sklearn требует форму (samples, features), поэтому делаем reshape
        state_reshaped = state.reshape(1, -1)

        # Актор выбирает базовый объем заказа
        mu = actor.predict(state_reshaped)[0]
        mu = max(0.0, mu)  # Аналог Softplus на выходе

        # Добавляем шум для исследования (exploration)
        action = mu + np.random.normal(0, 2.0)
        action = max(0.0, action)

        # Шаг в среде
        next_state, reward = env.step(action)
        epoch_reward += reward

        next_state_reshaped = next_state.reshape(1, -1)

        # Оценка критика для текущего и следующего состояния
        v_current = critic.predict(state_reshaped)[0]
        v_next = critic.predict(next_state_reshaped)[0]

        # Расчет временной разности (TD-error)
        td_target = reward + gamma * v_next
        td_error = td_target - v_current

        # --- Шаг 1. Обновление Критика (MSE Loss) ---
        # Обучаем критика точнее предсказывать ценность состояния V(s) -> td_target
        critic.partial_fit(state_reshaped, np.array([td_target]))

        # --- Шаг 2. Обновление Актора (Policy Gradient аналог) ---
        # Если td_error > 0, выбранное действие было хорошим -> двигаем mu в сторону action.
        # Если td_error < 0, действие было плохим -> двигаем mu в противоположную сторону.
        # Шаг сдвига пропорционален величине td_error.
        learning_rate_policy = 0.1
        actor_target = mu + learning_rate_policy * td_error * (action - mu)
        actor_target = np.array([max(0.0, actor_target)])

        actor.partial_fit(state_reshaped, actor_target)

        state = next_state

    rewards_history.append(epoch_reward / steps_per_epoch)

print("Обучение завершено.")

# --- 4. Визуализация ---
plt.figure(figsize=(10, 5))
plt.plot(
    rewards_history, color="blue", linewidth=1.5, label="Среднее подкрепление за шаг"
)
plt.title("График поступления подкрепления (Адаптивный Критик на scikit-learn)")
plt.xlabel("Эпоха обучения")
plt.ylabel("Величина подкрепления (Reward)")
plt.grid(True, linestyle="--", alpha=0.6)
plt.legend()
plt.show()
