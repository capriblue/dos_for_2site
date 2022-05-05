import numpy as np


class System:
    def __init__(self, t: float, L: int, S: int):
        self.L = L
        self.S = S
        self.t = t
        self.DeltaE = (self.Emax - self.Emin) / self.L
        self.Eaxis = np.linspace(self.Emin, self.Emax, L)

        self.Emax = 2 * self.t
        self.Emin = - 2 * self.t
        self.Mean = 4 / np.pi * self.t

    def delta_func(self, x):
        if -self.DeltaE <= x and x < 0:
            return 1 / self.DeltaE
        else:
            return 0


class OneDimSystem(System):
    def __init__(self, t: float, L: int, S: int):
        self.Dim = 1
        super().__init__(t, L, S)
        self.N = self.__calc_N()

    def Eigen(self, n):
        return - 2 * self.t * (np.cos(2 * np.pi * n / self.N))

    def __calc_one_state(self, E):
        result = 0
        for n in range(self.N):
            result += self.delta_func(E - self.system.Eigen(n))
        return result

    def calc_dos(self):
        calc_func = np.vectorize(self.__calc_one_state, otypes=[float])
        self.DOS = calc_func(self.Eaxis)
        return self.DOS

    def __calc_N(self):
        return int((self.S * self.L * 2 * np.pi * self.Mean / (self.Emax - self.Emin))**(1/self.Dim))


class TwoDimSystem(System):
    def __init__(self, t: float, L: int, S: int):
        self.Dim = 2
        super().__init__(t, L, S)
        self.N = self.__calc_N()

    def Eigen(self, n, m):
        return -2 * self.t * (np.cos(2 * np.pi * n / self.N) + np.cos(2 * np.pi * m / self.N))

    def __calc_one_state(self, E):
        result = 0
        for n in range(self.N):
            for m in range(self.N):
                result += self.delta_func(E - self.system.Eigen(n, m))
        return result

    def calc_dos(self):
        calc_func = np.vectorize(self.__calc_one_state, otypes=[float])
        self.DOS = np.sum(calc_func(self.Eaxis))
        return self.DOS

    def __calc_N(self):
        return int((self.S * self.L * 2 * np.pi * self.Mean / (self.Emax - self.Emin))**(1/self.Dim))


class ThreeDimSystem(System):
    def __init__(self, t: float, L: int, S: int):
        self.Dim = 3
        super().__init__(t, L, S)
        self.__calc_N()

    def Eigen(self, n, m, l):
        return -2 * self.t * (np.cos(2 * np.pi * n / self.N) + np.cos(2 * np.pi * m / self.N) + np.cos(2 * np.pi * l / self.N))

    def __calc_one_state(self, E):
        result = 0
        for n in range(self.N):
            for m in range(self.N):
                for l in range(self.N):
                    result += self.delta_func(E - self.system.Eigen(n, m, l))
        return result

    def calc_dos(self):
        calc_func = np.vectorize(self.__calc_one_state, otypes=[float])
        self.DOS = np.sum(calc_func(self.Eaxis))
        return self.DOS

    def __calc_N(self):
        return int((self.S * self.L * 2 * np.pi * self.Mean / (self.Emax - self.Emin))**(1/self.Dim))
