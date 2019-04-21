import unittest

from amdgpu_fan.lib.amdgpu import Card


pwm_max = 250
pwm_min = 0


class MockEndpoint:
    def __init__(self, value=None):
        self.value = value


class MockCard(Card):
    def __init__(self, card_identifier):
        self._endpoints = dict(
            temp1_input=MockEndpoint(),
            pwm1_max=MockEndpoint(pwm_max),
            pwm1_min=MockEndpoint(pwm_min),
            pwm1_enable=MockEndpoint(),
            pwm1=MockEndpoint()
        )

    def read_endpoint(self, endpoint):
        return self._endpoints[endpoint].value

    def write_endpoint(self, endpoint, data):
        self._endpoints[endpoint].value = data


class TestCard(unittest.TestCase):
    def setUp(self) -> None:
        self.card = MockCard('card1')
        self.card._verify_card()

    def test_mocked_temp_input(self):
        for val in range(1, 100):
            self.card._endpoints['temp1_input'].value = val * 1000
            self.assertEqual(self.card.gpu_temp, val)

    def test_mocked_pwm_max(self):
        self.assertEqual(self.card.fan_max, pwm_max)
        for speed in range(-10, 110):
            self.card.set_fan_speed(speed)
            self.assertLessEqual(self.card.read_endpoint('pwm1'), pwm_max)
            self.assertGreaterEqual(self.card.read_endpoint('pwm1'), pwm_min)
