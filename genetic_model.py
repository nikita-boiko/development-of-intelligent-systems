import numpy as np
import random

# 1. Генерация тестовых данных (курс валюты за 100 дней)
np.random.seed(42)
history_data = np.sin(np.linspace(0, 10, 100)) + np.random.normal(0, 0.1, 100) + 75.0

# Настройки алгоритма согласно условиям
NUM_BANKS = 3  # Количество банков (популяций) >= 3
POP_SIZE = 50  # Количество особей в банке >= 50
EPOCHS = 3  # Количество эпох (поколений) >= 3
PREV_DAYS = 5  # Сколько предыдущих дней учитываем (длина хромосомы)
MUTATION_RATE = 0.1  # Вероятность мутации

# 2. Инициализация популяций (банков)
# Каждая особь — это массив из 5 весов + смещение (всего 6 генов)
banks = []
for _ in range(NUM_BANKS):
    bank = np.random.uniform(-1, 1, (POP_SIZE, PREV_DAYS + 1))
    banks.append(bank)


# 3. Функция оценки точности (Фитнес-функция)
# Чем меньше среднеквадратичная ошибка (MSE), тем выше приспособленность (1 / (1 + MSE))
def calculate_fitness(individual, data):
    error_sum = 0
    count = 0
    for i in range(PREV_DAYS, len(data)):
        window = data[i - PREV_DAYS : i]
        # Линейный прогноз: веса * значения + смещение
        predicted = np.dot(individual[:-1], window) + individual[-1]
        actual = data[i]
        error_sum += (predicted - actual) ** 2
        count += 1
    mse = error_sum / count
    return 1 / (1 + mse)


# 4. Основной цикл генетического алгоритма
for epoch in range(1, EPOCHS + 1):
    print(f"\n--- ЭПОХА {epoch} ---")

    for b_idx in range(NUM_BANKS):
        current_bank = banks[b_idx]

        # Расчет фитнеса для всех особей в банке
        fitness_scores = np.array(
            [calculate_fitness(ind, history_data) for ind in current_bank]
        )

        # Вывод лучшего результата в банке
        best_idx = np.argmax(fitness_scores)
        best_mse = (1 / fitness_scores[best_idx]) - 1
        print(
            f"Банк {b_idx + 1}: Лучший фитнес = {fitness_scores[best_idx]:.6f} (MSE: {best_mse:.4f})"
        )

        # Селекция (Рулетка)
        prob = fitness_scores / np.sum(fitness_scores)
        selected_indices = np.random.choice(POP_SIZE, size=POP_SIZE, p=prob)
        new_population = current_bank[selected_indices].copy()

        # Скрещивание (Кроссинговер) и Мутация
        for i in range(0, POP_SIZE, 2):
            if i + 1 < POP_SIZE:
                # Одноточечный кроссинговер
                crossover_point = random.randint(1, PREV_DAYS)
                parent1, parent2 = (
                    new_population[i].copy(),
                    new_population[i + 1].copy(),
                )

                new_population[i][:crossover_point] = parent1[:crossover_point]
                new_population[i][crossover_point:] = parent2[crossover_point:]
                new_population[i + 1][:crossover_point] = parent2[:crossover_point]
                new_population[i + 1][crossover_point:] = parent1[crossover_point:]

        # Мутация
        for ind in new_population:
            if random.random() < MUTATION_RATE:
                mutation_idx = random.randint(0, PREV_DAYS)
                ind[mutation_idx] += np.random.normal(0, 0.1)

        banks[b_idx] = new_population

    # Миграция между банками (обмен лучшими особями в конце эпохи)
    for b_idx in range(NUM_BANKS):
        next_bank_idx = (b_idx + 1) % NUM_BANKS
        # Находим лучшего в текущем банке
        scores = np.array(
            [calculate_fitness(ind, history_data) for ind in banks[b_idx]]
        )
        best_ind = banks[b_idx][np.argmax(scores)]

        # Заменяем худшего в следующем банке
        next_scores = np.array(
            [calculate_fitness(ind, history_data) for ind in banks[next_bank_idx]]
        )
        worst_idx = np.argmin(next_scores)
        banks[next_bank_idx][worst_idx] = best_ind
