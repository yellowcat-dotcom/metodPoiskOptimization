import pchely_D
import numpy
from math import pi

# Определение функций
def sphere_function(x, y):
    return x * x + y * y

def rastrigin_function(x, y):
    return 20 + (x * x - 10 * numpy.cos(2 * pi * x) + y * y - 10 * numpy.cos(2 * pi * y))

def schwefel_function(x, y):
    return (-x * numpy.sin(numpy.sqrt(numpy.abs(x)))) + (-y * numpy.sin(numpy.sqrt(numpy.abs(y))))

# Определение функции для симуляции алгоритма на сфере
def lab4_sphere(dimension=2, iterCount=300, swarmsize=200):
    # Установка граничных значений для координат
    number_of_points = 1000
    left_border, right_border = -100, 100
    minvalues = numpy.array([left_border] * dimension)
    maxvalues = numpy.array([right_border] * dimension)

    # Установка параметров алгоритма для сферы
    currentVelocityRatio = 0.1
    localVelocityRatio = 1.0
    globalVelocityRatio = 5.0

    # Инициализация объекта класса SwarmSphere
    swarm = pchely_D.SwarmSphere(swarmsize,
                        minvalues,
                        maxvalues,
                        currentVelocityRatio,
                        localVelocityRatio,
                        globalVelocityRatio)

    # Списки для хранения результатов
    x, y, z = [], [], []
    # Итерации алгоритма
    for n in range(iterCount):
        x.append(swarm.globalBestPosition[0])
        y.append(swarm.globalBestPosition[1])
        z.append(swarm.globalBestFinalFunc)

        # Вызов следующей итерации PSO
        swarm.nextIteration()

    # Возвращение результатов
    return [sphere_function, x, y, z, left_border, right_border, number_of_points]

def lab4_rastrigin(dimension=2, iterCount=200, swarmsize=200):
        number_of_points = 1000
        left_border, right_border = -5.12, 5.12
        minvalues = numpy.array([left_border] * dimension)
        maxvalues = numpy.array([right_border] * dimension)

        currentVelocityRatio = 0.5
        localVelocityRatio = 2.0
        globalVelocityRatio = 5.0

        swarm = pchely_D.SwarmRastrigin(swarmsize,
                               minvalues,
                               maxvalues,
                               currentVelocityRatio,
                               localVelocityRatio,
                               globalVelocityRatio
                               )

        x, y, z = [], [], []
        for n in range(iterCount):
            x.append(swarm.globalBestPosition[0])
            y.append(swarm.globalBestPosition[1])
            z.append(swarm.globalBestFinalFunc)

            swarm.nextIteration()

        return [rastrigin_function, x, y, z, left_border, right_border, number_of_points]

def lab4_schwefel(dimension=2, iterCount=200, swarmsize=500):
        number_of_points = 1000
        left_border, right_border = -500, 500
        minvalues = numpy.array([left_border] * dimension)
        maxvalues = numpy.array([right_border] * dimension)

        currentVelocityRatio = 0.5
        localVelocityRatio = 2.0
        globalVelocityRatio = 5.0

        swarm = pchely_D.SwarmSchwefel(swarmsize,
                              minvalues,
                              maxvalues,
                              currentVelocityRatio,
                              localVelocityRatio,
                              globalVelocityRatio)

        x, y, z = [], [], []
        for n in range(iterCount):
            x.append(swarm.globalBestPosition[0])
            y.append(swarm.globalBestPosition[1])
            z.append(swarm.globalBestFinalFunc)

            swarm.nextIteration()

        return [schwefel_function, x, y, z, left_border, right_border, number_of_points]

