import time
import os_shared
import json
from dataclasses import dataclass, asdict
from hw_board import HWBoard
from appconfig import SftrailsConfig, SftrailsSensorTimers



def sensors_watchdog(hwboard: HWBoard, config: SftrailsConfig, stop_event):
    """
    This functions is used to watch and collect sensor data
    Args:
        hwboard (HWBoard):  Hardware Description 
        config (SftrailsConfig): Configuration of the application
        stop_event (Event): Event that inidicate to exit the loop and finish the function
    """
    sleep_time, err = config.get_sensor_time(SftrailsSensorTimers.SENSOR_DATA)
    if sleep_time == 0:
        print(err)
        return

    while not stop_event.is_set():
        with hwboard.shtc3.lock:
            hwboard.shtc3.update_sensor_data()
            temp, humi = hwboard.shtc3.get_sensor_data()
            print(json.dumps(asdict(temp), indent=4))
            print(json.dumps(asdict(humi), indent=4))
        with hwboard.pac1945.lock:
            hwboard.pac1945.update_sensor_data()
            print(json.dumps(asdict(hwboard.pac1945.get_sensor_data()), indent=4))
        with hwboard.ads1115.lock:
            hwboard.ads1115.update_sensor_data()
            print(json.dumps(asdict(hwboard.ads1115.get_sensor_data()), indent=4))
        with hwboard.pt100.lock:
            hwboard.pt100.update_sensor_data()
            print(json.dumps(asdict(hwboard.pt100.get_sensor_data()), indent=4))
        time.sleep(sleep_time)


def rail_gpio_watchdog(hwboard: HWBoard, config: SftrailsConfig, stop_event):
    """
    This functions is used to watch the BARRA IN gpio event, if the event is true
    play the sound to inform that the barra in event is detect
    Args:
        hwboard (HWBoard):  Hardware Description 
        config (SftrailsConfig): Configuration of the application
        stop_event (Event): Event that inidicate to exit the loop and finish the function
    """
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
    """
    This functions is used to watch the PTAs gpio events
    Args:
        hwboard (HWBoard):  Hardware Description 
        config (SftrailsConfig): Configuration of the application
        stop_event (Event): Event that inidicate to exit the loop and finish the function
    """
    sleep_time, err = config.get_sensor_time(SftrailsSensorTimers.PTA_CHECK)
    if sleep_time == 0:
        print(err)
        return

    while not stop_event.is_set():
        with hwboard.gpio_lock:
            print(f'PTA1 value {hwboard.pta1.get_value()}')
            print(f'PTA2 value {hwboard.pta2.get_value()}')
        time.sleep(sleep_time)
