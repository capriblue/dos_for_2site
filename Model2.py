import matplotlib.pyplot as plt
import numpy as np
class Calculate:
    def __init__(self, dimension, time, Emin, Emax, dens: bool = True):
        self.dens = dens
        self.L = 1000
        self.N = int(time**(1/dimension))
        self.dim = dimension
        self.L = 1000
        self.Es = np.linspace(Emin, Emax, self.L)
        self.hist = self.__get_hist()

    def N_dim_sumation(self, one_dim_array):
        def __pinch_it_with_bracket(content, times):
            for _ in range(times - 1):
                content = [content]
            return content

        result = __pinch_it_with_bracket(np.copy(one_dim_array), 1)
        for times in range(2, self.dim + 1):
            result = result + np.array(
                __pinch_it_with_bracket(
                    np.copy(one_dim_array),
                    times
                )
            ).T
        return result

    def get_eigens(self):
        return self.N_dim_sumation(
            np.cos(2 * np.pi / self.N * np.arange(self.N))
        )

    def __get_hist(self):
        place = np.searchsorted(self.Es, self.get_eigens())
        hist = np.histogram(place, bins=np.arange(
            self.L + 1), density=self.dens)
        return hist[0]

if __name__ == "__main__":
    twoD = Calculate(3, 1000000000, -3, 3, False)
    plt.plot(twoD.Es, twoD.hist)
