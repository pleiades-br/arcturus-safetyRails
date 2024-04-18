import espeak
import dtmf
import gpiod
import subprocess
import pyaudio
import wave
import argparse
from datetime import datetime, timedelta
from gpiod.line import Edge, Direction, Value, Bias

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

def main():
    '''
        Argument parsing with argparse and main job
    '''
    #GPIO pin to enable
    gpio_pin_enable = 5

    # GPIO pin to monitor
    gpio_pin_monitor = 1

    # Request lines to configure and monitoring
    with gpiod.request_lines(
            path="/dev/gpiochip0",
            consumer='Safety-Rail',
            config={
                gpio_pin_monitor:
                    gpiod.LineSettings(
                        direction=Direction.INPUT,
                        active_low=True,
                        edge_detection=Edge.BOTH,
                        bias=Bias.PULL_UP,
                        debounce_period=timedelta(seconds=0.5)
                ),
                gpio_pin_enable: 
                    gpiod.LineSettings (
                        direction=Direction.OUTPUT,
                        output_value=Value.ACTIVE
                )
            }
        ) as line:
            while True:
                # Block until rising edge event happens
                if line.read_edge_events():
                     print("State change %d", line.get_value(gpio_pin_monitor))

if __name__ == '__main__':
    main()
