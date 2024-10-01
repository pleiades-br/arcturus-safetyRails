import os
import pyaudio
import wave
import argparse
from datetime import datetime, timedelta
from sensors import Sensors

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
    try:
        while data:
            stream.write(data)
            data = wf.readframes(CHUNK)
    except Exception as error:
        print(f'Not possible to play filename {file}. Error {type(error).__name__} - {error}')

    # Close the stream and PyAudio
    stream.stop_stream()
    stream.close()
    p.terminate()

def play_with_aplay(filename):
    cmd = f'aplay {filename}'
    os.system(cmd)

def main():
    '''
        Argument parsing with argparse and main job
    '''
    sensor = Sensors()
    temp, humi = sensor.shtc3.get_sensor_data()
    print(f'Sensor data {temp}:{humi}%')
    data = sensor.pt100.get_sensor_data()
    print(f'Pt100 data {data}')

if __name__ == '__main__':
    main()
