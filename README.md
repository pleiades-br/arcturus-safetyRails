
# Safety Rails - GPIO Monitoring

## Overview

This project is specific for arcturus project. The main functionality are: look for the GPIO state 
and executing some sound acording the project specification.

## Features

- Choose the gpiochip and one gpio number to monitor
- Plays audio when an event occur
- Adjustable parameters such as tone text pitch, gap, volume, speed and others.

## Usage

### Generating synthesis speech from an input string

The full command below show how you can start the main process

```bash
sftrails <dtmf_pre> <string_text> <dtmf_pro> <int_gpiochip> <int_gpionum  --text-pitch <text_pitch> --text-gap <text_gap> --text-capitals <1=sound | 2=the word> --text-speed <text_speed> --text-volume <text_volume> --text-male-voice --dtmf-duration <dtmf_duration> --dtmf-silence-duration <silence_duration> --dtmf-sample-rate <sample_rate>
```

## Configuration

Adjustable parameters in the script:

--text-pitch: Pitch adjustment, 0 to 99, *(default: 32)* <br>
--text-gap: Word gap. Pause between words, units of 10mS at the default speed. *(default: 1)* <br>
--text-capitals: Indicate capital letters with: 1=sound, 2=the word "capitals" *(default: 1)* <br>
--text-speed: Speed in approximate words per minute. The default is 175 *(default: 175)* <br>
--text-volume: Volume, 0 to 200, *(default: 100)* <br>
--text-male-voice: Use a male voice instead a female voice <br>
--dtmf-duration: Duration of each tone in milliseconds *(default: 500)* <br>
--dtmf-silence-duration: Duration of silence between tones in milliseconds *(default: 25)* <br>
--dtmf-sample-rate: Sample rate in Hz *(default: 8000)*. <br>

## Testing

You can start to monitor a gpio pad and play the correspondent audio using the example command below:

```bash
sftrails ACB12 "Testing 1 2 3" AC723 4 20
```

## Dependencies

### System dependencies

- espeak (v1.48): Old espeak library.

```bash
apt install -y espeak
```

### Python dependencies

- NumPy: For numerical operations;
- Pyaudio: Playing the wav files;
- Gpiod: Python interface for controls gpios.

```bash
pip install -r requirements.txt
```

## Contributing

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
