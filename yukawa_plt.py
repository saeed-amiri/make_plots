import numpy as np
import matplotlib.pylab as plt
import matplotlib

class Doc:
    """plot Yukawa potential
    """

def yukawa(g: float,  # coeff
           r: tuple[float, float, float]  # interval of the data
           ) -> tuple[list[float], list[float]]:
    """return a tuple of two list contains the x and y"""
    print(r[0])
    x: list[float] = np.linspace(r[0], r[1], r[2])*0.1
    y: list[float] = g*np.exp(-x)/x
    return x, y

def plot_yukawa(x: list[float],  # x intervales
                y: list[float]  # yukawa values
                ) -> None:
    """plot the yukawa"""

if __name__ == '__main__':
    x, y = yukawa(1, (1, 10, 100))
    print(x, y)