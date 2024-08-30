from espeak import ESpeak
from dtmf import DTMF
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

def gpio_loop(gpio_chip, gpio_pin_monitor):
    # Request lines to configure and monitoring
    try:
        with gpiod.request_lines(
                path=gpio_chip,
                consumer='Safety-Rail',
                config={
                    gpio_pin_monitor:
                        gpiod.LineSettings(
                            direction=Direction.INPUT,
                            edge_detection=Edge.BOTH,
                            bias=Bias.PULL_DOWN,
                            debounce_period=timedelta(seconds=0.5)
                    )
                }
            ) as line:
                while True:
                    # Block until rising edge event happens
                    if line.read_edge_events():
                        if (line.get_value(gpio_pin_monitor) == Value.INACTIVE):
                            print("SafteyRails detect Alarm on rail sensor")
                            play("dtmf_pre.wav")
                            play("text_output.wav")
                            play("dtmf_pos.wav")
    except Exception as error:
        print(f'Not possible to initialize gpio num {gpio_pin_monitor} monitoring in {gpio_chip} \
              Error {type(error).__name__} - {error}')



def gpio_chip_range_checker(arg):
    MIN_VAL = 0
    MAX_VAL = 4
    """ 
    Type function for argparse - a int within some predefined bounds 
    """
    try:
        value = int(arg)
    except ValueError:    
        raise argparse.ArgumentTypeError("Must be a int point number")
    if value < MIN_VAL or value > MAX_VAL:
        raise argparse.ArgumentTypeError("Argument must be < " + str(MAX_VAL) + "and > " + str(MIN_VAL))
    return value

def gpio_num_range_checker(arg):
    MIN_VAL = 0
    MAX_VAL = 31
    """ 
    Type function for argparse - a int within some predefined bounds 
    """
    try:
        value = int(arg)
    except ValueError:    
        raise argparse.ArgumentTypeError("Must be a int point number")
    if value < MIN_VAL or value > MAX_VAL:
        raise argparse.ArgumentTypeError("Argument must be < " + str(MAX_VAL) + "and > " + str(MIN_VAL))
    return value

def main():
    '''
        Argument parsing with argparse and main job
    '''
    parser = argparse.ArgumentParser(description='Prove of concept for Arcturus project')
    parser.add_argument('dtmf_pre', type=str, help='Sequence of digits to generate preamble DTMF tones.')
    parser.add_argument('text', type=str, help='String used to transform to audio')
    parser.add_argument('dtmf_pos', type=str, help='Sequence of digits to generate preamble DTMF tones.')
    parser.add_argument('gpiochip', type=gpio_chip_range_checker, help='Gpiochip where the monitored gpio is connected (int value)')
    parser.add_argument('gpionum', type=gpio_num_range_checker, help='Gpio number to monitored (int value)')
    parser.add_argument('--text-pitch', type=int, default=30, help=' Pitch adjustment, 0 to 99, default is 32')
    parser.add_argument('--text-gap', type=int, default=1, help=' Word gap. Pause between words, units of 10mS at the default speed')
    parser.add_argument('--text-capitals', type=int, default=1, help='Indicate capital letters with: 1=sound, 2=the word "capitals"')
    parser.add_argument('--text-speed', type=int, default=125, help=' Speed in approximate words per minute. The default is 175')
    parser.add_argument('--text-volume', type=int, default=100, help='Volume, 0 to 200, default is 100')
    parser.add_argument('--text-male-voice', action='store_true', help='Use a male voice instead a female voice')
    parser.add_argument('--dtmf-duration', type=int, default=500, help='Duration of each tone in milliseconds (default: 500).')
    parser.add_argument('--dtmf-silence-duration', type=int, default=25, help='Duration of silence between tones in milliseconds (default: 25).')
    parser.add_argument('--dtmf-sample-rate', type=int, default=8000, help='Sample rate in Hz (default: 8000).')
    args = parser.parse_args()

    dtmf_o = DTMF(duration=args.dtmf_duration, silence_duration=args.dtmf_silence_duration,
                    sample_rate=args.dtmf_sample_rate)
    dtmf_o.generate_dtmf_tones(args.dtmf_pre)
    dtmf_o.save_wave_file(filename="dtmf_pre.wav")

    dtmf_o.generate_dtmf_tones(args.dtmf_pos)
    dtmf_o.save_wave_file(filename="dtmf_pos.wav")

    engine = ESpeak(volume=args.text_volume, gap=args.text_gap, capitals=args.text_capitals, 
                    pitch=args.text_pitch, speed=args.text_speed, male_voice=args.text_male_voice)
    
    engine.save_wave_file(args.text,filename="text_output.wav")

    #GPIO pin to enable
    gpio_chip = f'/dev/gpiochip{args.gpiochip}'

    # GPIO pin to monitor
    gpio_pin_monitor = args.gpionum

    gpio_loop(gpio_chip, gpio_pin_monitor)


if __name__ == '__main__':
    main()
