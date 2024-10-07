import os
import threading
from datetime import datetime, timedelta
from sensors import Sensors
from arcturus_gpios import ArcturusGpios
from watchers import rail_gpio_watchdog

def play_with_aplay(filename):
    cmd = f'aplay {filename}'
    os.system(cmd)

def main():
    '''
        Argument parsing with argparse and main job
    '''
    #sensor = Sensors()
    railgpio = ArcturusGpios(3, 20, "rail")
    thread1 = threading.Thread(target=rail_gpio_watchdog, args=(railgpio, 10, False))
    thread1.start()
    thread1.join()

if __name__ == '__main__':
    main()
