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
        return yaml.load(f)


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

    CMD_HELP = """usage: amdgpu-fan [COMMAND] [ARGS] [CARD]
        
CARD should be what shows up in /sys/class/drm. If there's only one card (ex: card0), it will be automatically detected.
    
commands:
    --start         start fan control
    --get           get information about the card
    --set-speed     set gpu fan speed
            
args:
    with --get:
        fan_speed   get the current speed of the fan
        gpu_temp    get the current temp of the gpu
            
    with --set-speed:
        input the speed you'd like from 0-100 or auto
        100 = max, 0 = off, 'auto' = system controlled
"""

    args = sys.argv[1:]
    if '--help' in args or '-h' in args or len(args) == 0\
            or args[0] not in ('--start', '--get', '--set-speed')\
            or (args[0] == '--get' and (args[1] not in ('fan_speed', 'gpu_temp'))):
        print(CMD_HELP)
        sys.exit(1)

    scanner = Scanner()

    command = args[0]
    if len(args) > 1:
        arg = args[1]
    if len(args) < 3:
        cards = Scanner(config.get('cards')).cards
        if len(cards) > 1:
            print("There are two or more cards. Please specify the card you wish to examine.")
            print(list(card.keys()))
            sys.exit(1)
        else:
            card = list(cards.keys())[0]
    else:
        card = args[2]

    if command == '--get':
        if arg == 'fan_speed':
            print(f"{scanner.cards.get(card).fan_speed} rpm")
        elif arg == 'gpu_temp':
            print(f"{scanner.cards.get(card).gpu_temp} °C")

    elif command == '--set-speed':
        if arg == 'auto':
            scanner.cards.get(card).set_system_controlled_fan(True)
        else:
            print(scanner.cards.get(card).set_fan_speed(arg))
    elif command == '--start':
        FanController(config).main()

    sys.exit(1)

if __name__ == '__main__':
    main()
