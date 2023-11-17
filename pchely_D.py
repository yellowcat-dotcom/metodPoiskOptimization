import numpy
import numpy.random

from abc import ABCMeta, abstractmethod

import numpy.random

#описывает поведение частицы на каждом шаге итерации.
class Particle(object):
    def __init__(self, swarm):
        self.__currentPosition = self.__getInitPosition(swarm)
        self.__localBestPosition = self.__currentPosition[:]
        self.__localBestFinalFunc = swarm.getFinalFunc(self.__currentPosition)
        self.__velocity = self.__getInitVelocity(swarm)

    @property
    def position(self):
        return self.__currentPosition

    @property
    def velocity(self):
        return self.__velocity

    def __getInitPosition(self, swarm):
        return numpy.random.rand(swarm.dimension) * (swarm.maxvalues - swarm.minvalues) + swarm.minvalues

    def __getInitVelocity(self, swarm):
        assert len(swarm.minvalues) == len(self.__currentPosition)
        assert len(swarm.maxvalues) == len(self.__currentPosition)

        minval = -(swarm.maxvalues - swarm.minvalues)
        maxval = (swarm.maxvalues - swarm.minvalues)

        return numpy.random.rand(swarm.dimension) * (maxval - minval) + minval

    def nextIteration(self, swarm):
        # Случайный вектор для коррекции скорости с учетом лучшей позиции данной частицы
        rnd_currentBestPosition = numpy.random.rand(swarm.dimension)
        # Случайный вектор для коррекции скорости с учетом лучшей глобальной позиции всех частиц
        rnd_globalBestPosition = numpy.random.rand(swarm.dimension)

        veloRatio = swarm.localVelocityRatio + swarm.globalVelocityRatio
        commonRatio = (2.0 * swarm.currentVelocityRatio /
                       (numpy.abs(2.0 - veloRatio - numpy.sqrt(veloRatio ** 2 - 4.0 * veloRatio))))

        # Посчитать новую скорость
        newVelocity_part1 = commonRatio * self.__velocity
        newVelocity_part2 = (commonRatio *
                             swarm.localVelocityRatio *
                             rnd_currentBestPosition *
                             (self.__localBestPosition - self.__currentPosition))
        newVelocity_part3 = (commonRatio *
                             swarm.globalVelocityRatio *
                             rnd_globalBestPosition *
                             (swarm.globalBestPosition - self.__currentPosition))

        self.__velocity = newVelocity_part1 + newVelocity_part2 + newVelocity_part3

        # Обновить позицию частицы
        self.__currentPosition += self.__velocity

        finalFunc = swarm.getFinalFunc(self.__currentPosition)
        if self.__localBestFinalFunc == None or finalFunc < self.__localBestFinalFunc:
            self.__localBestPosition = self.__currentPosition[:]
            self.__localBestFinalFunc = finalFunc


class Swarm(object):
    __metaclass__ = ABCMeta

    def __init__(self,
                 swarmsize, # размер роя
                 minvalues, # список, задающий минимальные значения для каждой координаты
                 maxvalues, # список, задающий максимальные значения для каждой координаты частицы
                 currentVelocityRatio, # общий масштабирующий коэффициент для скорости
                 localVelocityRatio, # коэффициент, задающий влияние лучшей точки, найденной каждой частицей, на будущую скорость
                 globalVelocityRatio ):# коэффициент, задающий влияние лучшей точки, найденной всеми частицами, на будущую скорость


        self.__swarmsize = swarmsize

        assert len(minvalues) == len(maxvalues)
        assert (localVelocityRatio + globalVelocityRatio) > 4

        self.__minvalues = numpy.array(minvalues[:])
        self.__maxvalues = numpy.array(maxvalues[:])

        self.__currentVelocityRatio = currentVelocityRatio
        self.__localVelocityRatio = localVelocityRatio
        self.__globalVelocityRatio = globalVelocityRatio

        self.__globalBestFinalFunc = None
        self.__globalBestPosition = None

        self.__swarm = self.__createSwarm()

    def __getitem__(self, index):
        return self.__swarm[index]

    def __createSwarm(self):
        return [Particle(self) for _ in range(self.__swarmsize)]

    def nextIteration(self):
        for particle in self.__swarm:
            particle.nextIteration(self)

    @property
    def minvalues(self):
        return self.__minvalues

    @property
    def maxvalues(self):
        return self.__maxvalues

    @property
    def currentVelocityRatio(self):
        return self.__currentVelocityRatio

    @property
    def localVelocityRatio(self):
        return self.__localVelocityRatio

    @property
    def globalVelocityRatio(self):
        return self.__globalVelocityRatio

    @property
    def globalBestPosition(self):
        return self.__globalBestPosition

    @property
    def globalBestFinalFunc(self):
        return self.__globalBestFinalFunc

    def getFinalFunc(self, position):
        assert len(position) == len(self.minvalues)

        finalFunc = self._finalFunc(position)

        if (self.__globalBestFinalFunc is None or
                finalFunc < self.__globalBestFinalFunc):
            self.__globalBestFinalFunc = finalFunc
            self.__globalBestPosition = position[:]

    @abstractmethod
    def _finalFunc(self, position):
        pass

    @property
    def dimension(self):
        return len(self.minvalues)

    def _getPenalty(self, position, ratio):
        penalty1 = sum([ratio * abs(coord - minval)
                        for coord, minval in zip(position, self.minvalues)
                        if coord < minval])

        penalty2 = sum([ratio * abs(coord - maxval)
                        for coord, maxval in zip(position, self.maxvalues)
                        if coord > maxval])

        return penalty1 + penalty2


class SwarmSphere(Swarm):
    def __init__(self,
                 swarmsize,
                 minvalues,
                 maxvalues,
                 currentVelocityRatio,
                 localVelocityRatio,
                 globalVelocityRatio):
        Swarm.__init__(self,
                       swarmsize,
                       minvalues,
                       maxvalues,
                       currentVelocityRatio,
                       localVelocityRatio,
                       globalVelocityRatio)

    def _finalFunc(self, position):
        penalty = self._getPenalty(position, 10000.0)
        finalfunc = sum(position * position)

        return finalfunc + penalty


class SwarmRastrigin(Swarm):
    def __init__(self,
                 swarmsize,
                 minvalues,
                 maxvalues,
                 currentVelocityRatio,
                 localVelocityRatio,
                 globalVelocityRatio):
        Swarm.__init__(self,
                       swarmsize,
                       minvalues,
                       maxvalues,
                       currentVelocityRatio,
                       localVelocityRatio,
                       globalVelocityRatio)

    def _finalFunc(self, position):
        function = 10.0 * len(self.minvalues) + sum(position * position - 10.0 * numpy.cos(2 * numpy.pi * position))
        penalty = self._getPenalty(position, 10000.0)

        return function + penalty


class SwarmSchwefel(Swarm):
    def __init__(self,
                 swarmsize,
                 minvalues,
                 maxvalues,
                 currentVelocityRatio,
                 localVelocityRatio,
                 globalVelocityRatio):
        Swarm.__init__(self,
                       swarmsize,
                       minvalues,
                       maxvalues,
                       currentVelocityRatio,
                       localVelocityRatio,
                       globalVelocityRatio)

    def _finalFunc(self, position):
        function = sum(-position * numpy.sin(numpy.sqrt(numpy.abs(position))))
        penalty = self._getPenalty(position, 10000.0)
        return function + penalty