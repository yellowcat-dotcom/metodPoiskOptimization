import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import minimize

from mpl_toolkits.mplot3d import Axes3D
def simplex_function(x1, x2):
    return 2 * x1 ** 2 + 3 * x2 ** 2 + 4 * x1 * x2 - 6 * x1 - 3 * x2

def start_simplex():
    columns = ["x1", "x2", "lmbd", "lmbd2" "v1", "v2"]
    rows = ["z1", "z2", "w", "w2"]
    variables = ["x1", "x2"]

    matrix = [[4, 4, 1, 2, -1, 0, 6],
              [4, 6, 1, 3, 0, -1, 3],
              [1, 1, 0, 0, 0, 0, 1],
              [2, 3, 0, 0, 0, 0, 4],
              [8, 10, 2, 5, -1, -1, 3]]

    result = [get_simplex_result(matrix, rows, columns, variables)]
    return result

def get_simplex_result(matrix, rows, columns, variables):
    while True:
        row, column = get_resolution_row_column(matrix)
        if row == -1:
            res = []
            for variable in variables:
                row_index = get_variable_index(rows, variable)
                if row_index != -1:
                    res.append(matrix[row_index][-1])

            res.append(simplex_function(res[0], res[1]))
            return res

        change_matrix(matrix, rows, columns, row, column)

def get_resolution_row_column(matrix):
    mx = 0
    column_index = -1

    for i in range(0, len(matrix[-1]) - 1):
        if matrix[-1][i] > mx:
            mx = matrix[-1][i]
            column_index = i

    if column_index == -1:
        return [-1, -1]

    mn = matrix[0][-1] / matrix[0][column_index]
    row_index = 0

    for i in range(1, len(matrix) - 1):
        if mn > matrix[i][-1] / matrix[i][column_index] > 0:
            mn = matrix[i][-1] / matrix[i][column_index]
            row_index = i

    return [row_index, column_index]


def change_matrix(matrix, rows, columns, resolution_row, resolution_column):
    matrix[resolution_row][resolution_column] **= -1
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


def get_variable_index(rows, variable):
    for i in range(len(rows)):
        if rows[i] == variable:
            return i

    return -1

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

    print(x)
    return simplex_function, x, y, z, left_border, right_border, number_of_points

def fun(x_i):  # Функция
    x1 = x_i[0]
    x2 = x_i[1]
    return 2 * x1 * x1 + 3 * x2 * x2 + 4 * x1 * x2 - 6 * x1 - 3 * x2

def callback(x_w):
    g_list = np.ndarray.tolist(x_w)
    g_list.append(fun(x_w))
    points.append(g_list)

points = []
def example():
    b = (0, float("inf"))  # диапазон поиска
    bounds = (b, b)
    x0 = (10, 15)  # начальная точка
    con = {'type': 'eq', 'fun': fun}

    # основной вызов
    res = minimize(fun, x0, method="SLSQP", bounds=bounds,
                   constraints=con, callback=callback)
    optimal_solution = res.x
    optimal_value = res.fun
    return optimal_solution, optimal_value

def main():
    if __name__ == '__main__':
     main()



