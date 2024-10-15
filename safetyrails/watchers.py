import time
from hw_board import HWBoard


def play_with_aplay(filename):
    cmd = f'aplay {filename}'
    os.system(cmd)


def sensors_watchdog(hwboard: HWBoard, sleep_time: int, stop_event):
    while not stop_event.is_set():
        with hwboard.shtc3.lock:
            print(hwboard.shtc3.get_sensor_data())
        with hwboard.pac1945.lock:
            print(hwboard.pac1945.get_sensor_data())
        with hwboard.ads1115.lock:
            print(hwboard.ads1115.get_sensor_data())
        with hwboard.pt100.lock:
            print(hwboard.pt100.get_sensor_data())
        time.sleep(sleep_time)


def rail_gpio_watchdog(hwboard: HWBoard, sleep_time: int, stop_event):
    while not stop_event.is_set():
        with hwboard.gpio_lock:
            print(f'rail value {hwboard.barra_in.get_value()}')
        time.sleep(sleep_time)


def ptas_gpio_watchog(hwboard: HWBoard, sleep_time: int, stop_event):
    while not stop_event.is_set():
        with hwboard.gpio_lock:
            print(f'PTA1 value {hwboard.pta1.get_value()}')
            print(f'PTA2 value {hwboard.pta2.get_value()}')
        time.sleep(sleep_time)
