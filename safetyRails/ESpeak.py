import subprocess

class ESpeak(object):
    def __init__(self,
                 volume     = 100,
                 device     = None,
                 gap        = -1,
                 capitals   = 1,
                 pitch      = 50,
                 speed      = 175,
                 male_voice = False,
                 voice      = 'pt') -> None:
        self._volume = volume
        self._device = device
        self._gap = gap
        self._capitals = capitals
        self._pitch = pitch
        self._speed = speed
        self._male_voice = male_voice
        self._voice = voice

    @property
    def volume(self):
        return self._volume
    @volume.setter
    def volume(self, v):
        self._volume = v

    @property
    def device(self):
        return self._device
    @device.setter
    def device(self, v):
        self._device = v

    @property
    def gap(self):
        return self._gap
    @gap.setter
    def gap(self, v):
        self._gap = v

    @property
    def capitals(self):
        return self._capitals
    @capitals.setter
    def capitals(self, v):
        self._capitals = v

    @property
    def pitch(self):
        return self._pitch
    @pitch.setter
    def pitch(self, v):
        self._pitch = v

    @property
    def speed(self):
        return self._speed
    @speed.setter
    def speed(self, v):
        self._speed = v

    @property
    def male_voice(self):
        return self._male_voice
    @male_voice.setter
    def male_voice(self, v):
        self._male_voice = v

    @property
    def voice(self):
        return self._voice
    @voice.setter
    def voice(self, v):
        self._voice = v

    def _espeak_exe(self, args):
        '''
            Execute the espeak application to generate the sintetic voice
        '''
        cmd = ['espeak', 
            '-a', str(self._volume),
            '-k', str(self._capitals), 
            '-p', str(self._pitch), 
            '-s', str(self._speed), 
            '-b', '1', # UTF8 text encoding 
            ]
        
        if self._gap >= 0:
            cmd.extend(['-g', str(self._gap)])

        if self._male_voice == False:
            voice = self._voice + '+f2'
        else:
            voice = self._voice + '+m2'
        
        cmd.extend(['-v', voice])

        cmd.extend(args)

        p = subprocess.Popen(cmd,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.STDOUT)
        
        res = iter(p.stdout.readline, b'')

        p.stdout.close()
        p.wait()

        return res
    
    def say(self, txt):
        args = []

        if self._device:
            pass
        else:
            args.extend(['-w', "output_speech.wav"])

        args.append(txt.encode('utf8'))

        return self._espeak_exe(args)
    
    def save_wave_file(self, txt, filename="output_speech.wav"):
        args = []

        args.extend(['-w', filename])
        args.append(txt.encode('utf8'))

        return self._espeak_exe(args)
    
