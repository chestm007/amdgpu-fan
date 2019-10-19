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
        self.curve = Curve(config.get('speed_matrix'))
        self._frequency = 1

    def main(self):
        logger.info(f'starting amdgpu-fan')
        while True:
            for name, card in self._scanner.cards.items():
                temp = card.gpu_temp
                speed = int(self.curve.get_speed(int(temp)))
                if speed < 0:
                    speed = 0

                logger.debug(f'{name}: Temp {temp}, Setting fan speed to: {speed}, fan speed{card.fan_speed}, min:{card.fan_min}, max:{card.fan_max}')

                card.set_fan_speed(speed)
            time.sleep(self._frequency)


def load_config(path):
    logger.debug(f'loading config from {path}')
    with open(path) as f:
        return yaml.safe_load(f)


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
