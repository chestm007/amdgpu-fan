import os
import sys
import time

import yaml

from amdgpu_fan import LOGGER as logger
from amdgpu_fan.lib.amdgpu import Scanner
from amdgpu_fan.lib.curve import Curve

CONFIG_LOCATIONS = [
    '/etc/amdgpu-fan.yml',
]


class FanController:
    def __init__(self, config):
        self._scanner = Scanner(config.get('cards'))
        if len(self._scanner.cards) < 1:
            logger.error('no compatible cards found, exiting')
            sys.exit(1)
        speed_matrix = config.get('speed_matrix')
        self.temp_drop  = config.get('temp_drop', 5)
        self.curve = Curve(speed_matrix)
        self._frequency = 1
        self._interval = 1/self._frequency

    def main(self):
        logger.info(f'starting amdgpu-fan')
        speed_by_card = {}
        while True:
            for name, card in self._scanner.cards.items():
                current_speed = speed_by_card.get(name)
                temp = card.gpu_temp

                speed = max(0, int(self.curve.get_speed(int(temp))))
                if current_speed is not None and current_speed >= speed:
                    speed = max(0, int(self.curve.get_speed(int(temp) + self.temp_drop)))
                    if current_speed <= speed:
                        continue

                logger.debug(f'{name}: Temp {temp}, Setting fan speed to: {speed}, fan speed: {card.fan_speed}, min: {card.fan_min}, max: {card.fan_max}')

                card.set_fan_speed(speed)
                speed_by_card[name] = speed

            time.sleep(self._interval)


def load_config(path):
    logger.debug(f'loading config from {path}')
    with open(path) as f:
        return yaml.safe_load(f, Loader=yaml.FullLoader)


def main():

    default_fan_config = '''#Fan Control Matrix. [<Temp in C>,<Fanspeed in %>]
speed_matrix:
- [0, 0]
- [30, 33]
- [45, 50]
- [60, 66]
- [65, 69]
- [70, 75]
- [75, 89]
- [80, 100]

# optional
# cards:  # can be any card returned from `ls /sys/class/drm | grep "^card[[:digit:]]$"`
# - card0

# optional
# temp_drop: 5  # how much temperature should drop before fan speed is decreased
'''
    config = None
    for location in CONFIG_LOCATIONS:
        if os.path.isfile(location):
            config = load_config(location)
            break

    if config is None:
        logger.info(f'no config found, creating one in {CONFIG_LOCATIONS[-1]}')
        with open(CONFIG_LOCATIONS[-1], 'w') as f:
            f.write(default_fan_config)
            f.flush()

        config = load_config(CONFIG_LOCATIONS[-1])

    FanController(config).main()


if __name__ == '__main__':
    main()
