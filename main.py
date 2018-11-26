import time
import configparser
import requests
import random
from phue import Bridge


def get_ip_from_config():
    config = configparser.ConfigParser()
    config.read('philips.conf')
    return config['DEFAULT']['bridge_ip']


def get_username_from_config():
    config = configparser.ConfigParser()
    config.read('philips.conf')
    return config['DEFAULT']['username']


def get_ark_price():
    return requests.get('https://min-api.cryptocompare.com/data/price?fsym=ARK&tsyms=USD').json()['USD']


def main(b):
    lights = b.get_light_objects()
    for light in lights:
        light.brightness(255)
        light.xy = [random.random(), random.random()]


if __name__ == '__main__':
    bridge = Bridge(get_ip_from_config(), get_username_from_config())
    # If running for the first time press button on bridge and run with bridge.connect()
    bridge.connect()
    while True:
        print(get_ark_price())
        time.sleep(10)

