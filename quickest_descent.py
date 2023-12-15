# /use/bin/env python3
# coding: UTF-8

from scipy import optimize


# собственно функция
def func(x, y):
    return (x ** 2 + y - 11) ** 2 + (x + y ** 2 - 7) ** 2


# её градиент в конкретной точке
def gradient(x, y):
    dx = 4 * x ** 3 + 4 * x * y - 42 * x + 2 * y ** 2 - 14
    dy = 2 * x ** 2 + 4 * y ** 3 - 22 + 4 * x * y - 26 * y
    return [dx, dy]


# норма градиента (сравнивается с точностью)
def norm(grad):
    return grad[0] ** 2 + grad[1] ** 2


# Списки, чтобы их можно было изменять глобально
cur_grad = [0, 0]
cur_point = [0, 0]


# Эту функцию будем минимизировать на каждом шаге
def func_t(t):
    return func(cur_point[0] - t * cur_grad[0], cur_point[1] - t * cur_grad[1])


'''
Параметры:
1-2. Координаты начальной точки
3. Максимальное количество итераций
4. Погрешность для градиента
5. Погрешность для функции
'''


def quickest_descent(x0, y0, iterations, ep1, ep2):
    list_points = list()
    x = x0
    y = y0
    cur_point[0] = x
    cur_point[1] = y
    result = False
    cur_val = func(x, y)
    # итерации
    k = 0
    while not result:
        list_points.append([x, y, cur_val])
        currentGradient = gradient(x, y)
        cur_grad[0] = currentGradient[0]
        cur_grad[1] = currentGradient[1]
        gradNorm = norm(currentGradient)
        if gradNorm < ep1 or k >= iterations:
            xres = x0
            yres = y0
            result = True
        else:
            cur_t = optimize.minimize(func_t, [0])
            new_x = x - cur_t.x[0] * cur_grad[0]
            new_y = y - cur_t.x[0] * cur_grad[1]
            # alpha = 0.00000001  # Постоянный шаг, можно выбрать другое значение
            # new_x = x - alpha * cur_grad[0]
            # new_y = y - alpha * cur_grad[1]


            list_points.append([new_x, new_y, func(new_x, new_y)])
            new_val = func(x, y)
            if norm([new_x - x, new_y - y]) < ep2 and abs(cur_val - new_val) < ep2:
                xres = x0
                yres = y0
                result = True
            else:
                k += 1
                x = new_x
                y = new_y
                cur_val = new_val
                cur_point[0] = x
                cur_point[1] = y

    # print(cur_point, cur_val)
    list_points.append([cur_point[0], cur_point[1], cur_val])
    return list_points
