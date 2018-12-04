import requests
import configparser


def get_ark_price():
    return requests.get('https://min-api.cryptocompare.com/data/price?fsym=ARK&tsyms=USD').json()['USD']


def get_from_config(key):
    config = configparser.ConfigParser()
    config.read('philips.conf')
    return config['DEFAULT'][key]
