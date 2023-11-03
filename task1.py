
import numpy as np
import matplotlib.pyplot as plt


# Определение функции f(x)
def f(x):
    return 2 * x[0] ** 2 + x[0] * x[1] + x[1] ** 2

# Градиент функции f(x)
def gradient_f(x):
    return np.array([4 * x[0] + x[1], x[0] + 2 * x[1]])

# Гессиан функции f(x)
def hessian(x):
    return np.array([[4, 1], [1, 2]])

def task_1(x1, x2, M, epsilon1, epsilon2,tk):
    # Начальное значение x
    x = np.array([x1, x2])

    # Создание трехмерной сетки для визуализации поверхности
    x1_vals = np.linspace(-10, 10, 10)
    x2_vals = np.linspace(-10, 10, 10)
    X1, X2 = np.meshgrid(x1_vals, x2_vals)
    Z = 2 * X1 ** 2 + X1 * X2 + X2 ** 2

    # Переменные для хранения истории значений x и f(x)
    x_history = [x]
    fx_history = [f(x)]

    k = 0

    while True:
        if k >= M:
            break

        # Вычисление новой точки x^(k+1)
        x_new = x - tk * gradient_f(x)

        while f(x_new) - f(x) >= 0:
            tk /= 2
            x_new = x - tk * gradient_f(x)

        x = x_new

        x_history.append(x)
        fx_history.append(f(x))

        # Проверка достаточных условий минимума
        hess = hessian(x)
        if np.linalg.det(hess) > 0:
            print(f" {x} удовлетворяет условию (H(x^k) > 0).")

        if np.linalg.norm(x_history[-1] - x_history[-2]) < epsilon2 and np.linalg.norm(
                fx_history[-1] - fx_history[-2]) < epsilon2:
            break

        k += 1

    x_history = np.array(x_history)
    fx_history = np.array(fx_history)
    # Вывод результатов
    print(f"Минимум в точке x* = {x}")
    print(f"Значение функции f(x*) = {f(x)}")

    # Визуализация трехмерной поверхности функции f(x)
    fig = plt.figure(figsize=(12, 8))
    ax = fig.add_subplot(111, projection='3d')
    ax.plot_surface(X1, X2, Z, cmap='viridis')
    ax.set_xlabel('x1')
    ax.set_ylabel('x2')
    ax.set_zlabel('f(x)')
    ax.set_title('Градиентный спуск - Поверхность функции f(x)')

    # Добавление следа градиентного спуска
    ax.plot(x_history[:, 0], x_history[:, 1], fx_history, marker='o', linestyle='-', color='red', label='Градиентный спуск')
    ax.legend()

    fig.set_size_inches(6,4)

    # Вывод результатов
    return fig, f"Минимум в точке x* = {x}"+"\n"+ f"Значение функции f(x*) = {f(x)}"

