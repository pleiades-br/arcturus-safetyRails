import os
import threading
from datetime import datetime, timedelta
from hw_board import HWBoard
from watchers import rail_gpio_watchdog, sensors_watchdog, ptas_gpio_watchog

def play_with_aplay(filename):
    cmd = f'aplay {filename}'
    os.system(cmd)

def main():
    '''
        Argument parsing with argparse and main job
    '''

    hwboard = HWBoard()
    thread1 = threading.Thread(target=rail_gpio_watchdog, args=(hwboard, 5, False))
    thread2 = threading.Thread(target=sensors_watchdog, args=(hwboard, 15, False))
    thread3 = threading.Thread(target=ptas_gpio_watchog, args=(hwboard, 10, False))

    thread1.start()
    thread2.start()
    thread3.start()
    thread1.join()
    thread2.join()
    thread3.join()

if __name__ == '__main__':
    main()