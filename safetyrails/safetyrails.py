import espeak
import dtmf
import gpiod
import subprocess
import pyaudio
import wave
import argparse
import time

def play(file):
    CHUNK = 1024

    # Open the audio file
    wf = wave.open(file, 'rb')

    # Initialize PyAudio
    p = pyaudio.PyAudio()

    # Open a stream
    stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                    channels=wf.getnchannels(),
                    rate=wf.getframerate(),
                    output=True)

    # Read data
    data = wf.readframes(CHUNK)

    # Play the audio
    while data:
        stream.write(data)
        data = wf.readframes(CHUNK)

    # Close the stream and PyAudio
    stream.stop_stream()
    stream.close()
    p.terminate()

def gpio_loop(gpio):
    try:
        # Initial state
        previous_state = gpio.get_value()
        while True:
            # Read current state
            current_state = gpio.get_value()

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
    gpio = gpiod.request_lines(
        "/dev/gpiochip0",
        consumer="Trail",
        config= {
            gpio_pin: gpiod.LineSettings (
                direction=gpiod.line.Direction.INPUT
            )
        }
    )

    gpio_loop(gpio)
    gpio.release()

    return 0

if __name__ == '__main__':
    main()
    