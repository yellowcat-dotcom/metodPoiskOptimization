import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Определение функции, которую мы оптимизируем
def simplex_function(x1, x2):
    return 2 * x1 ** 2 + 2 * x1 * x2 + 2 * x2 ** 2 - 4 * x1 - 6 * x2

# Начальная инициализация симплекс-метода
def start_simplex():
    columns = ["x1", "x2", "lmbd", "v1", "v2"]
    rows = ["z1", "z2", "w"]
    variables = ["x1", "x2"]

    # Исходная матрица
    matrix = [[4, 2, 1, -1, 0, 4],
              [2, 4, 2, 0, -1, 6],
              [1, 2, 0, 0, 0, 2],
              [6, 6, 3, -1, -1, 10]]

    result = [get_simplex_result(matrix, rows, columns, variables)]
    return result

# Получение оптимального решения методом симплекса
def get_simplex_result(matrix, rows, columns, variables):
    while True:
        # Находим разрешающий столбец и строку
        row, column = get_resolution_row_column(matrix)
        if row == -1:
            # Если не существует разрешающего элемента, возвращаем оптимальное решение
            res = []
            for variable in variables:
                row_index = get_variable_index(rows, variable)
                if row_index != -1:
                    res.append(matrix[row_index][-1])

            res.append(simplex_function(res[0], res[1]))
            return res
        # Изменяем матрицу после нахождения разрешающего элемента
        change_matrix(matrix, rows, columns, row, column)

# Получение строки и столбца для разрешающего элемента
def get_resolution_row_column(matrix):
    mx = 0
    column_index = -1

    # Находим столбец с максимальным значением в последней строке матрицы
    for i in range(0, len(matrix[-1]) - 1):
        if matrix[-1][i] > mx:
            mx = matrix[-1][i]
            column_index = i

    if column_index == -1: #критерий останова
        return [-1, -1]

    mn = matrix[0][-1] / matrix[0][column_index]
    row_index = 0

    # Находим строку с минимальным положительным отношением в предпоследнем столбце матрицы
    for i in range(1, len(matrix) - 1):
        if mn > matrix[i][-1] / matrix[i][column_index] > 0:
            mn = matrix[i][-1] / matrix[i][column_index]
            row_index = i

    return [row_index, column_index]

# Изменение матрицы после нахождения разрешающего элемента
def change_matrix(matrix, rows, columns, resolution_row, resolution_column):
    matrix[resolution_row][resolution_column] **= -1 #приближаем значение к единице
    for i in range(0, len(matrix)):
        for j in range(0, len(matrix[0])):
            if i != resolution_row and j != resolution_column:
                matrix[i][j] = matrix[i][j] - (matrix[resolution_row][j] * matrix[i][resolution_column])\
                               * matrix[resolution_row][resolution_column]

    for i in range(0, len(matrix[resolution_row])):
        if i != resolution_column:
            matrix[resolution_row][i] *= matrix[resolution_row][resolution_column]

    for i in range(0, len(matrix)):
        if i != resolution_row:
            matrix[i][resolution_column] *= -matrix[resolution_row][resolution_column]

    rows[resolution_row], columns[resolution_column] = columns[resolution_column], rows[resolution_row]

# Получение индекса переменной в списке строк
def get_variable_index(rows, variable):
    for i in range(len(rows)):
        if rows[i] == variable:
            return i

    return -1

# Функция для построения графика функции в 3D
def lab2():
    points = start_simplex()

    x, y, z = [], [], []
    for point in points:
        x.append(point[0])
        y.append(point[1])
        z.append(point[2])

    left_border = -6
    right_border = 6
    number_of_points = 1000

    return simplex_function, x, y, z, left_border, right_border, number_of_points

# Основная функция, которая будет вызвана при запуске программы
def main():
    print(2)

if __name__ == '__main__':
    main()
