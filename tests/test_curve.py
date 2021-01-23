import unittest

from amdgpu_fan.lib.curve import Curve


class TestCurve(unittest.TestCase):
    def test_linear_curve(self):
        curve = Curve([[4, 4], [100, 100]])
        for speed in range(4, 100):
            self.assertEqual(speed, curve.get_speed(speed))

