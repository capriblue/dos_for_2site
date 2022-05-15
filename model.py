import numpy as np

class Calculate:
    def __init__(self, dimension, time, Emin, Emax, dens: bool = True, L: int = 300):
        self.dens = dens
        self.L = 300
        self.N = int( time**(1/dimension))
        self.dim = dimension
        self.Es = np.linspace(Emin, Emax, self.L)
        self.hist = self.__get_hist()
    def N_dim_sumation(self, one_dim_array):
        result = np.array(np.copy(one_dim_array))
        for times in range(2, self.dim + 1):
            result = result + np.array(np.copy(one_dim_array), ndmin=times).T
        return result
    
    def get_eigens(self):
        return self.N_dim_sumation(
            np.cos( 2 * np.pi /self.N * np.arange(self.N))
            )

    def __get_hist(self):
        place =  np.searchsorted(self.Es, self.get_eigens())
        hist = np.histogram(place, bins=np.arange(self.L + 1), density=self.dens)
        return hist[0]
def domp(x,y, filename):
    data = np.c_[x,y]
    np.savetxt(filename, data, delimiter=",")


if __name__ == "__main__":
    two = Calculate(2, 10000000000, -2, 2, True)
    domp(two.Es[1:], two.hist[1:], "two")
    three