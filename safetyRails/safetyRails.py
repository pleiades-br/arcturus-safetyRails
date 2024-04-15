import ESpeak 
import DTMF
from gpiozero import DigitalInputDevice
import subprocess
import simpleaudio as sa
import argparse
import time

def play(file):
    wave_obj = sa.WaveObject.from_wave_file(file)
    play_obj = wave_obj.play()
    play_obj.wait_done()

def gpio_loop(gpio_device):
    try:
        # Initial state
        previous_state = gpio_device.value
        while True:
            # Read current state
            current_state = gpio_device.value

            # Check if state has changed
            if current_state != previous_state:
                print("Previous state: %d \nCurrent State %d", previous_state, current_state)
                # Update previous state
                previous_state = current_state

            # Wait before checking again
            time.sleep(0.1)

    except KeyboardInterrupt:
        pass  # KeyboardInterrupt will be caught, allowing proper cleanup

def main():
    '''
        Argument parsing with argparse and main job
    '''
    # GPIO pin to monitor
    gpio_pin = 1

    # Create DigitalInputDevice object for the GPIO pin
    gpio_device = DigitalInputDevice(gpio_pin)

    gpio_loop(gpio_device)
    gpio_device.close()

if __name__ == "__main__":
    main()