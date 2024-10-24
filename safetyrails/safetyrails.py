import os
import threading
import time
import argparse
from hw_board import HWBoard
from watchers import rail_gpio_watchdog, sensors_watchdog, ptas_gpio_watchog
from appconfig import SftrailsConfig
from mqtt_client import mqtt_thread


def argument_parser() -> str:
    '''
        Argument parsing with argparse and main job
    '''
    parser = argparse.ArgumentParser(description='Rail sensors watchdog')
    parser.add_argument(
        '--config-file', 
        type=str,
        default='/etc/sftrails/sftrails.conf',
        help='Path/filename to the config file'
    )

    args = parser.parse_args()
    return args.config_file

def main():
    '''
        Main application
    '''
    stop_event = threading.Event()
    appconf = SftrailsConfig(file_path=argument_parser())
    hwboard = HWBoard()

    thread1 = threading.Thread(target=rail_gpio_watchdog, args=(hwboard, appconf, stop_event))
    thread2 = threading.Thread(target=sensors_watchdog, args=(hwboard, appconf, stop_event))
    thread3 = threading.Thread(target=ptas_gpio_watchog, args=(hwboard, appconf, stop_event))
    thread4 = threading.Thread(target=mqtt_thread, args=(hwboard, appconf, stop_event))
    thread1.start()
    thread2.start()
    thread3.start()
    thread4.start()

    try:
        while not stop_event.is_set():
            time.sleep(1)  # Simulate doing some work in the main thread
    except KeyboardInterrupt:
        print("Interrupt by user!")
    finally:
        stop_event.set()

    thread1.join()
    thread2.join()
    thread3.join()
    thread4.join()
    appconf.write_config_to_file()

if __name__ == '__main__':
    main()
