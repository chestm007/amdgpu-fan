import unittest

from amdgpu_fan.lib.curve import Curve


class TestCurve(unittest.TestCase):
    def test_linear_curve(self):
        curve = Curve([[0, 0], [100, 100]])
        for speed in range(0, 100):
            self.assertEqual(speed, curve.get_speed(speed))

