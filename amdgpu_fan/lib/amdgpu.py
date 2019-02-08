import os
import re
import sys

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
        with open(self._endpoints[endpoint], 'w') as e:
            return e.write(str(data))

    @property
    def fan_speed(self):
        return int(self.read_endpoint('fan1_input'))

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
        if speed > self.fan_max:
            speed = self.fan_max
        elif speed < self.fan_min:
            speed = self.fan_min
        speed = self.fan_max / 100 * speed
        self.set_system_controlled_fan(False)
        return self.write_endpoint('pwm1', int(speed))


class Scanner:
    CARD_REGEX = '^card\d$'

    def __init__(self):
        self.cards = self._get_cards()

    def _get_cards(self):
        """
        only directories in ROOT_DIR that are card1, card0, card3 etc.
        :return: a list of initialized Card objects
        """
        cards = {}
        for node in os.listdir(ROOT_DIR):
            if re.match(self.CARD_REGEX, node):
                try:
                    cards[node] = Card(node)
                except FileNotFoundError:
                    # if card lacks hwmon its likely not amdgpu, and definitely not compatible with this software
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
