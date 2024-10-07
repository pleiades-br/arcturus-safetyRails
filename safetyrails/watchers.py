import time
from hw_board import HWBoard

def sensors_watchdog(hwboard: HWBoard, sleep_time: int, finish: bool):
    while finish is False:
        with hwboard.shtc3.lock:
            print(hwboard.shtc3.get_sensors_data())
        time.sleep(sleep_time)


def rail_gpio_watchdog(hwboard: HWBoard, sleep_time: int, finish: bool):
    while finish is False:
        with hwboard.gpio_lock:
            print(f'rail value {hwboard.barra_in.get_value()}')
        time.sleep(sleep_time)


def ptas_gpio_watchog(hwboard: HWBoard, sleep_time: int, finish: bool):
    while finish is False:
        with hwboard.gpio_lock:
            print(f'PTA1 value {hwboard.pta1.get_value()}')
        with hwboard.gpio_lock:
            print(f'PTA2 value {hwboard.pta2.get_value()}')
        time.sleep(sleep_time)