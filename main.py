import time
import sys
import atexit
from phue import Bridge
from helpers import get_ark_price, get_from_config


LOOP_TIME = int(get_from_config("loop_time"))
TRANSITION_TIME = int(get_from_config("transition_time"))
UP_COLOR = int(get_from_config("price_up_color"))
DOWN_COLOR = int(get_from_config("price_down_color"))


def set_brightness(_bridge):
    if int(get_from_config("brightness")) > 254:
        print("Brightness can't be greater than 254.")
        _bridge.set_light(1, 'bri', 254, transitiontime=4)
    else:
        _bridge.set_light(1, 'bri', int(get_from_config("brightness")), transitiontime=4)


def set_color(_bridge, _up_color, _down_color, _transition_time):
    if prices[-1] > prices[0]:
        if _up_color == 23848:
            _bridge.set_light(1, 'hue', 23848, transitiontime=_transition_time)
        else:
            _bridge.set_light(1, 'hue', _up_color, transitiontime=_transition_time)
    elif prices[-1] < prices[0]:
        if _down_color == 65044:
            _bridge.set_light(1, 'hue', 65044, transitiontime=_transition_time)
        else:
            _bridge.set_light(1, 'hue', _down_color, transitiontime=_transition_time)


def on_exit():
    bridge.set_light(1, "hue", initial_color)
    bridge.set_light(1, "on", False)


if __name__ == '__main__':
    bridge = Bridge(get_from_config("bridge_ip"))
    bridge.connect()
    bridge.set_light(get_from_config("light_id"), "on", True)
    set_brightness(bridge)

    initial_color = bridge.get_api()["lights"]["1"]["state"]["hue"]
    prices = (get_ark_price(), get_ark_price())

    atexit.register(on_exit)

    while True:
        try:
            set_color(bridge, UP_COLOR, DOWN_COLOR, TRANSITION_TIME)
            prices = (prices[-1], get_ark_price())
            time.sleep(LOOP_TIME)
        except KeyboardInterrupt:
            print("Program exiting")
            sys.exit(0)
