import os
from shared_linux_const import LINUX_SYS_I2C_PATH

class Pac1945():
    NAME="""AIN{mux1}"""
    RAW_FILE="""in_voltage{mux1}_raw"""

    def __init__(self, config_list: list) -> None:
        self.__channels: list = []
        self.__dirpath: str = ""
        self.__get_dirpath()
        self.__create_channel_list(config_list)

    def __get_dirpath(self):
        for dirs in os.listdir(LINUX_SYS_I2C_PATH):
            sensor_name_file = os.path.join(LINUX_SYS_I2C_PATH, dirs, 'name')
            if os.path.isfile(sensor_name_file):
                try:
                    with open(sensor_name_file, 'r') as file:
                        sensor_name = file.read().strip()
                        if sensor_name == 'pac1945_1':
                            for entry in os.listdir(os.path.join(LINUX_SYS_I2C_PATH, dirs)):
                                if entry.startswith('iio'):
                                    self.__dirpath = os.path.join(LINUX_SYS_I2C_PATH, dirs, entry)
                                    break
                except Exception:
                    continue

        if self.__dirpath == "":
            raise FileNotFoundError("Could not find pac1945_1 sys folder")

    def __create_channel_list(self, config_list: list):
        for entry in config_list:
            channel = {
                    "name": self.NAME.format(mux1=entry),
                    "raw_file": self.RAW_FILE.format(mux1=entry),
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
        self.__update_data()
        return self.__channels