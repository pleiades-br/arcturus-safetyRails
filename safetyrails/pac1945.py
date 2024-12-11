import os
from os_shared import LINUX_SYS_I2C_PATH
from sensor import Sensor, SensorData

class Pac1945(Sensor):
    """
    This class works with the data from pac1945
    Read the linux subsystem inside /sys and make all necessary
    data transformation

    Init args:
        sensor_name: The sensor name/nickname
        config: List if a dictionary of parameters {'name', 'ch1'}, 
                each one containing a given name for the pads and the channel config

    Raises:
        FileNotFound: When could not find the pac1945 inside /sys
    """

    NAME="""AIN{mux1}"""
    FILE="""in_voltage{mux1}_{filetype}"""


    def __init__(self, sensor_name: str, config: list) -> None:
        super().__init__(sensor_name)
        self.__channels: list = []
        self.__dirpath: str = ""
        self.__get_dirpath()
        self.__create_channel_list(config)

    def __get_dirpath(self):
        for dirs in os.listdir(LINUX_SYS_I2C_PATH):
            sensor_name_file = os.path.join(LINUX_SYS_I2C_PATH, dirs, 'name')
            if os.path.isfile(sensor_name_file):
                try:
                    with open(sensor_name_file, 'r') as file:
                        sensor_name = file.read().strip()
                        if sensor_name == 'pac1952_1':
                            for entry in os.listdir(os.path.join(LINUX_SYS_I2C_PATH, dirs)):
                                if entry.startswith('iio'):
                                    self.__dirpath = os.path.join(LINUX_SYS_I2C_PATH, dirs, entry)
                                    break
                except Exception:
                    continue

        if self.__dirpath == "":
            raise FileNotFoundError("Could not find pac1952_1 sys folder")

    def __create_channel_list(self, config: list):
        for entry in config:
            if 'name' not in entry or 'ch1' not in entry:
                print('pac1945: Channel config does not have the minimal parameters')
                continue

            channel = SensorData( 
                name=entry['name'],
                hw_name=self.NAME.format(mux1=entry['ch1']),
                raw_file=self.FILE.format(mux1=entry['ch1'],filetype="raw"),
                scale_file=self.FILE.format(mux1=entry['ch1'],filetype="scale"),
            )

            self.__channels.append(channel)

    def update_sensor_data(self):
        """
        Update sensor data
        """
        for channel in self.__channels:
            raw_file = os.path.join(self.__dirpath, channel.raw_file)
            scale_file = os.path.join(self.__dirpath, channel.scale_file)
            try:
                with open(raw_file,'r') as file: 
                    channel.raw_value = int(file.read().strip())

            except Exception:
                print(f"Pac1945 could not take data from {channel.name}")
                continue

            try:
                with open(scale_file,'r') as file: 
                    channel.scale_value = float(file.read().strip())

            except Exception:
                print(f"Pac1945 could not take data from {channel.name}")
                continue

            channel.value = channel.raw_value * channel.scale_value

    def get_sensor_data(self):
        """ Get sensor data
            
        Returns:
            dictionary: containing the raw and input data from the sensor.
        """
        return self.__channels

    def get_sensor_raw_value_as_dict(self):
        """
        Return a dictionary with the name of channel as key
        and the raw_value as value
        """
        return {f'{channel.name}': channel.raw_value for channel in self.__channels}
    
    def get_sensor_value_as_dict(self):
        """
        Return a dictionary with the name of channel as key
        and the raw_value as value
        """
        return {f'{channel.name}': channel.value for channel in self.__channels}
