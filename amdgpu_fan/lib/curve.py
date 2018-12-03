from matplotlib import pyplot as plt
import numpy as np
from scipy.interpolate import pchip as interpol


class Curve:
    """
    creates a fan curve based on user defined points
    """
    def __init__(self, points: list):
        # ensure the curve starts at 0, 0
        has_zero = False
        for point in points:
            if point[0] == 0:
                has_zero = True

        if not has_zero:
            points.insert(0, [0, 0])

        points.sort(key=lambda s: s[0])

        temps = []
        speeds = []
        for set_ in points:
            temps.append(set_[0])
            speeds.append(set_[1])

        self._array = []

        # this involved alot of stack overflow and admittedly im not 100% sure how it works
        # basically given a set of points it extrapolates that into a line consisting of one
        # point per degree.
        x = np.asarray(temps)
        y = np.asarray(speeds)
        pch = interpol(x, y)
        xx = np.linspace(x[0], x[-1], x[-1])
        line2d = plt.plot(xx, pch(xx), 'g-')
        self.temps = line2d[0].get_xdata()
        self.speeds = line2d[0].get_ydata()

    def get_speed(self, temp):
        """
        returns a speed for a given temperature
        :param temp: int
        :return:
        """
        if temp > len(self.speeds):
            temp = len(self.speeds)
        if temp <= 0:
            temp = 1
        return self.speeds[temp - 1]


if __name__ == '__main__':
    c = Curve([[10, 10], [20, 20], [30, 30], [70, 80], [80, 100]])
#    plt.show()
    print(c.get_speed(60))
    print(c.get_speed(50))
    print(c.get_speed(80))
    print(c.get_speed(0))
    plt.show()
