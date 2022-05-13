import numpy as np
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
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

class DealData:
    def __init__(self, dim, num: int =  220000000):
        if dim == 1:
            self.__one(num)
        elif dim == 2:
            self.__two(num)
        elif dim  == 3:
            self.__three(num)
        else:
            self.__other( num)
    
    def __one(self, num):
        def func( x, a, b):
            return a * 1/ np.sqrt( 1- ( x/b)**2)
        one = Calculate(1, num, -1, 1, True)
        
        popt, pcov = curve_fit(func, one.Es[1:-1], one.hist[1:-1]) # 発散する点を除外してcurve_fit
        fig = plt.figure(facecolor='#fafafa')
        ax = fig.add_subplot(111)
        ax.plot(one.Es[1:-1], one.hist[1:-1], label="data") # 外れ値を除外
        ax.plot(one.Es[1:-1], func(one.Es[1:-1], *popt), 'g--', label="fit: a=%5.3f, b=%5.3f" % tuple(popt))
        fig.suptitle("Density of states (1D) ")
        ax.set_xlabel("Energy")
        _ =ax.set_ylabel("DOS")
        ax.legend()
        fig.savefig("DOS_1d.png", dpi=400)
    
    def __two(self, num):
        # 2D
        two = Calculate(2, num, -2, 2, True) 
        fig = plt.figure(facecolor='#fafafa')
        ax = fig.add_subplot(111)
        ax.plot(two.Es[1:], two.hist[1:]) # 外れ値を除外
        fig.suptitle("Density of states (2D) ")
        ax.set_xlabel("Energy")
        _ =ax.set_ylabel("DOS")
        fig.savefig("DOS_2d.png", dpi=400)

    def __three(self,num):
        three = Calculate(3, num, -3, 3, True)
        fig = plt.figure(facecolor='#fafafa')
        ax = fig.add_subplot(111)
        ax.plot(three.Es[1:], three.hist[1:]) # 外れ値を除外
        fig.suptitle("Density of states (3D) ")
        ax.set_xlabel("Energy")
        _ =ax.set_ylabel("DOS")
        fig.savefig("DOS_3d.png", dpi=400)
    
    def __other(self, num):
        def plotter(dim):
            calc = Calculate(dim,num, -dim, dim, True)
            ax.plot(calc.Es[1:], calc.hist[1:], label="{}D".format(dim))

        fig = plt.figure(facecolor='#fafafa')
        ax = fig.add_subplot(111)
        fig.suptitle("Density of state(4~8D)")
        for i in range(4, 9):
            plotter(i)

        ax.set_xlabel("Energy")
        ax.set_ylabel("DOS")
        ax.legend()
        fig.savefig("DOS_4-8d.png", dpi=400)



if __name__ == "__main__":
    DealData(1)