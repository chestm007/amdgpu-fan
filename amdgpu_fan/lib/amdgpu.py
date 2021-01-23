import os
import re
import sys
from amdgpu_fan import LOGGER as logger

ROOT_DIR = '/sys/class/drm'
HWMON_DIR = 'device/hwmon'


class Card:
    HWMON_REGEX = '^hwmon\d$'

    def __init__(self, card_identifier):
        self._identifier = card_identifier

        for node in os.listdir(os.path.join(ROOT_DIR, self._identifier, HWMON_DIR)):
            if re.match(self.HWMON_REGEX, node):
                self._monitor = node
        self._endpoints = self._load_endpoints()

    def _verify_card(self):
        for endpoint in ('temp1_input', 'pwm1_max', 'pwm1_min', 'pwm1_enable', 'pwm1'):
            if endpoint not in self._endpoints:
                logger.info('skipping card: %s as its missing endpoint %s', self._identifier, endpoint)
                raise FileNotFoundError

    def _load_endpoints(self):
        _endpoints = {}
        _dir =os.path.join(ROOT_DIR, self._identifier, HWMON_DIR, self._monitor)
        for endpoint in os.listdir(_dir):
            if endpoint not in ('device', 'power', 'subsystem', 'uevent'):
                _endpoints[endpoint] = os.path.join(_dir, endpoint)
        return _endpoints

    def read_endpoint(self, endpoint):
        with open(self._endpoints[endpoint], 'r') as e:
            return e.read()

    def write_endpoint(self, endpoint, data):
        try:
            with open(self._endpoints[endpoint], 'w') as e:
                return e.write(str(data))
        except PermissionError:
            logger.error('Failed writing to devfs file, are you sure your running as root?')
            sys.exit(1)

    @property
    def fan_speed(self):
        try:
            return int(self.read_endpoint('fan1_input'))
        except KeyError:  # better to return no speed then explode
            return 0

    @property
    def gpu_temp(self):
        return float(self.read_endpoint('temp1_input')) / 1000

    @property
    def fan_max(self):
        return int(self.read_endpoint('pwm1_max'))

    @property
    def fan_min(self):
        return int(self.read_endpoint('pwm1_min'))

    def set_system_controlled_fan(self, state):
        self.write_endpoint('pwm1_enable', 0 if state else 1)

    def set_fan_speed(self, speed):
        if speed >= 100:
            speed = self.fan_max
        elif speed <= 0:
            speed = self.fan_min
        else:
            speed = self.fan_max / 100 * speed
        self.set_system_controlled_fan(False)
        return self.write_endpoint('pwm1', int(speed))


class Scanner:
    CARD_REGEX = '^card\d$'

    def __init__(self, cards=None):
        self.cards = self._get_cards(cards)

    def _get_cards(self, cards_to_scan):
        """
        only directories in ROOT_DIR that are card1, card0, card3 etc.
        :return: a list of initialized Card objects
        """
        cards = {}
        for node in os.listdir(ROOT_DIR):
            if re.match(self.CARD_REGEX, node):
                if cards_to_scan and node.lower() not in [c.lower() for c in cards_to_scan]:
                    continue
                try:
                    cards[node] = Card(node)
                except FileNotFoundError:
                    # if card lacks hwmon or the required devfs files, its likely not
                    # amdgpu, and definitely not compatible with this software
                    continue
        return cards


if __name__ == '__main__':
    CMD_HELP = """
    usage: python amdgpu.py [COMMAND] [CARD] [ARGS]

        CARD should be what shows up in /sys/class/drm

        commands:
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
            or args[0] not in ('--get', '--set-speed')\
            or (args[0] == '--get' and (args[2] not in ('fan_speed', 'gpu_temp'))):
        print(CMD_HELP)
        sys.exit(1)

    try:
        command = args[0]
        card = args[1]
        arg = args[2]
    except IndexError:
        print(CMD_HELP)
        sys.exit(1)

    scanner = Scanner()

    if command == '--get':
        if arg == 'fan_speed':
            print(scanner.cards.get(card).fan_speed)
        elif arg == 'gpu_temp':
            print(scanner.cards.get(card).gpu_temp)

    elif command == '--set-speed':
        if arg == 'auto':
            scanner.cards.get(card).set_system_controlled_fan(True)
        else:
            print(scanner.cards.get(card).set_fan_speed(arg))
    sys.exit(1)
