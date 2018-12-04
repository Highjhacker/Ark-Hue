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
    bridge = Bridge(get_ip_from_config())
    # If running for the first time press button on bridge and run with bridge.connect()
    bridge.connect()
    bridge.set_light(1, 'bri', 254, transitiontime=4)

    prices = (get_ark_price(), get_ark_price())

    while True:
        print(prices)
        if prices[-1] > prices[0]:
            bridge.set_light(1, 'hue', 23848, transitiontime=4)
            print("Green")
        elif prices[-1] < prices[0]:
            bridge.set_light(1, 'hue', 65044, transitiontime=4)
            print("Red")
        else:
            print("No colors change")
        prices = (prices[-1], get_ark_price())
        time.sleep(5)


