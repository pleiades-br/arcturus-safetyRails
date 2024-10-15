import os
import configparser
from enum import Enum

class SftrailsSensorTimers(Enum):
    """
    Base Enum for access config without name dependency
    """
    SENSOR_DATA = 1
    BARRA_CHECK = 2
    PTA_CHECK = 3

class SftrailsConfig():
    """
    This class controls the config file for the safety rails application
    Init args:
        file_path: The path and the filename where the file.conf is located
                    if is not passed, the DEFAULT_PATH. If the file doesn't
                    exist a default configuration will be created on the 
                    file_path location

    Raises:
        FileNotFound: When an error trying to write in the file_path
    """
    CONFIG_PATH_FILE='/etc/sftrails/sftrail.conf'
    default_config = {
        'MQTT': {
            'host':'',
            'port':1883,
            'username':'',
            'password':'',
            'topic':'',
            'sleep_timer_s': 60,
        },

        'Sensor Timers': {
            'sensor_data_s': 15,
            'barra_in_check_s': 5,
            'ptas_s': 10,
        },

        'Alarm Sensor Thresholds':{
            'barra_v_check_mv': 4000,
            'barra_temperature_c': 60,
            'battery_mv': 10000,
            'solar_pannel': 4500
        },

        'Barra IN WAV': {
            'number_files': 3,
            'wav_file1': '',
            'wav_file2': '',
            'wav_file3': '',
            'wav_file4': '',
            'wav_file5': '',
        },
    }

    def __init__(self, file_path: str = ''):
        self.config = configparser.ConfigParser()
        self.file_path = self.CONFIG_PATH_FILE if file_path == '' else file_path
        if not os.path.exists(self.file_path):
            self.__create_default_config()

        self.config.read(self.file_path)

    def __create_default_config(self):
        """
        Create a config file with default parameters
        """
        self.config.read_dict(self.default_config)  # Load default parameters into the config object
        try:
            with open(self.file_path, 'w') as configfile:
                self.config.write(configfile)
            print(f"Default configuration created at {self.file_path}")
        except Exception as error:
            print(f'Not able to create the config file on {self.file_path}\n \
                   Error {type(error).__name__} - {error}')

    def write_config_to_file(self):
        """
        Write the current configuration to the file
        """
        try:
            with open(self.file_path, 'w') as configfile:
                self.config.write(configfile)
            print(f"Configuration written to {self.file_path}")
        except Exception as error:
            print(f'Not able to create the config file on {self.file_path}\n \
                   Error {type(error).__name__} - {error}')

    def update_config_value(self, section, key, value):
        """
        Update a specific value in the configuration
        """
        if not self.config.has_section(section):
            self.config.add_section(section)
        self.config.set(section, key, value)

    def get_sensor_time(self, key: int):
        """
        Return a specific value of a sensor timer inside config file
        also return a string containg any error that could occurr 
        """
        err = ''
        timer = 0
        section = 'Sensor Timers'

        if self.config.has_section(section):
            match key:
                case SftrailsSensorTimers.SENSOR_DATA:
                    timer = self.config.getint(section, 'sensor_data_s')
                case SftrailsSensorTimers.BARRA_CHECK:
                    timer = self.config.getint(section, 'barra_in_check_s')
                case SftrailsSensorTimers.PTA_CHECK:
                    timer = self.config.getint(section, 'ptas_s')
                case _:
                    err = f'Key {key} invalid for section {section}'
        else:
            err = 'Section "Sensor Timer" not found'
        return timer, err
