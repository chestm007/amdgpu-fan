import numpy as np


class Curve:
    """
    creates a fan curve based on user defined points
    """
    def __init__(self, points: list):
        self.points = np.array(points)
        self.temps = self.points[:, 0]
        self.speeds = self.points[:, 1]

        if np.min(self.speeds) < 0:
            raise ValueError(f'Fan curve contains negative speeds, speed should be in [0,100]')
        if np.max(self.speeds) > 100:
            raise ValueError(f'Fan curve contains speeds greater than 100, speed should be in [0,100]')
        if np.any(np.diff(self.temps) <= 0):
            raise ValueError(f'Fan curve points should be strictly monotonically increasing, configuration error ?')
        if np.any(np.diff(self.speeds) < 0):
            raise ValueError(f'Curve fan speeds should be monotonically increasing, configuration error ?')

    def get_speed(self, temp):
        """
        returns a speed for a given temperature
        :param temp: int
        :return:
        """

        return np.interp(x=temp, xp=self.temps, fp=self.speeds)


if __name__ == '__main__':
    c = Curve([[10, 10], [20, 20], [30, 30], [70, 80], [80, 100]])
    print(c.get_speed(60))
    print(c.get_speed(50))
    print(c.get_speed(80))
    print(c.get_speed(0))
