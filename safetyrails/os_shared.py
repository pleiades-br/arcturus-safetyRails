import os

LINUX_SYS_I2C_PATH = "/sys/bus/i2c/devices/"

def play_with_aplay(filename):
    """
    User aply to play a sound file
    Args:
        filename (str): path to the file
    """
    cmd = f'aplay {filename}'
    try:
        os.system(cmd)
    except Exception as error:
        print(f'Unable to play {filename} \n Error {type(error).__name__} - {error}')
