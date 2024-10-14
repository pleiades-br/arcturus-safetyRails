import os
import threading
import time
from hw_board import HWBoard
from watchers import rail_gpio_watchdog, sensors_watchdog, ptas_gpio_watchog

def play_with_aplay(filename):
    cmd = f'aplay {filename}'
    os.system(cmd)

def main():
    '''
        Argument parsing with argparse and main job
    '''
    stop_event = threading.Event()

    hwboard = HWBoard()
    thread1 = threading.Thread(target=rail_gpio_watchdog, args=(hwboard, 5, stop_event))
    thread2 = threading.Thread(target=sensors_watchdog, args=(hwboard, 15, stop_event))
    thread3 = threading.Thread(target=ptas_gpio_watchog, args=(hwboard, 10, stop_event))
    thread1.start()
    thread2.start()
    thread3.start()
    
    try:
        while not stop_event.is_set():
            time.sleep(1)  # Simulate doing some work in the main thread
    except KeyboardInterrupt:
        print(hwboard)
        print("Interrupt by user!")
    finally:
        stop_event.set()

    thread1.join()
    thread2.join()
    thread3.join()

if __name__ == '__main__':
    main()
