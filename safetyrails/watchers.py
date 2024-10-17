import time
from hw_board import HWBoard
from appconfig import SftrailsConfig, SftrailsSensorTimers
import os_shared 





def sensors_watchdog(hwboard: HWBoard, config: SftrailsConfig, stop_event):
    sleep_time, err = config.get_sensor_time(SftrailsSensorTimers.SENSOR_DATA)
    if sleep_time == 0:
        print(err)
        return

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


def rail_gpio_watchdog(hwboard: HWBoard, config: SftrailsConfig, stop_event):
    sleep_time, err = config.get_sensor_time(SftrailsSensorTimers.BARRA_CHECK)
    if sleep_time == 0:
        print(err)
        return

    files, err = config.get_wav_files()
    if err:
        print(err)

    while not stop_event.is_set():
        with hwboard.gpio_lock:
            value = hwboard.barra_in.get_value()
            if value is True:
                if hwboard.is_barra_in_alarm_sent is False and len(files) > 0:
                    for file in files:
                        os_shared.play_with_aplay(file)
                    hwboard.is_barra_in_alarm_sent = True
            else:
                hwboard.is_barra_in_alarm_sent = False

            print(f'rail value {value}')

        time.sleep(sleep_time)


def ptas_gpio_watchog(hwboard: HWBoard, config: SftrailsConfig, stop_event):
    sleep_time, err = config.get_sensor_time(SftrailsSensorTimers.PTA_CHECK)
    if sleep_time == 0:
        print(err)
        return

    while not stop_event.is_set():
        with hwboard.gpio_lock:
            print(f'PTA1 value {hwboard.pta1.get_value()}')
            print(f'PTA2 value {hwboard.pta2.get_value()}')
        time.sleep(sleep_time)
