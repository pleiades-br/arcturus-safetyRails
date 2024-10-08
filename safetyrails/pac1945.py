import os
from shared_linux_const import LINUX_SYS_I2C_PATH
from sensor import Sensor

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
    RAW_FILE="""in_voltage{mux1}_raw"""

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

            channel = {
                    "name": entry['name'],
                    "hw_name": self.NAME.format(mux1=entry['ch1']),
                    "raw_file": self.RAW_FILE.format(mux1=entry['ch1']),
                    "raw_value": 0,
                    "offset": 0
                }

            self.__channels.append(channel)

    def __update_data(self):
        for channel in self.__channels:
            try:
                with open(channel["raw_file"],'r') as file: 
                    channel["raw_value"] = int(file.read().strip())

            except Exception:
                print(f"Pac1945 could not take data from {channel['name']}")
                continue

    def get_sensor_data(self):
        """ Get an update sensor data
            
        Returns:
            dictionary: containing the raw and input data from the sensor.
        """
        self.__update_data()
        return self.__channels
