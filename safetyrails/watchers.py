import time
from sensors import Sensors
from arcturus_gpios import ArcturusGpios

def sensors_watchdog(sensors: Sensors, sleep_time: int, finish: bool):
    while finish is False:
        with sensors.lock:
            sensors.get_sensors_data()
        time.sleep(sleep_time)


def rail_gpio_watchdog(rail: ArcturusGpios, sleep_time: int, finish: bool):
    while finish is False:
        print(f'rail value {rail.get_value()}')
        time.sleep(sleep_time)
