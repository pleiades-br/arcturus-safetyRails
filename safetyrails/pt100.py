import os
from shared_linux_const import LINUX_SYS_I2C_PATH

class Pt100():
    NAME="""AIN{mux1}_AVSS"""
    RAW_FILE="""in_voltage{mux1}_raw"""
    INPUT_FILE="""in_voltage{mux1}_input"""
    MUX_NAME="""AIN{mux1}_AIN{mux2}"""
    MUX_RAW_FILE="""in_voltage{mux1}_in_voltage{mux2}_raw"""
    MUX_INPUT_FILE="""in_voltage{mux1}_in_voltage{mux2}_input"""

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
                        if sensor_name == 'ads122c04':
                            for entry in os.listdir(os.path.join(LINUX_SYS_I2C_PATH, dirs)):
                                if entry.startswith('iio'):
                                    self.__dirpath = os.path.join(LINUX_SYS_I2C_PATH, dirs, entry)
                                    break
                except Exception:
                    continue

        if self.__dirpath == "":
            raise FileNotFoundError("Could not find ti-ads122c04 sys folder")

    def __create_channel_list(self, config_list: list):
        for entry in config_list:
            channel = {}
            if isinstance(entry, list):
                channel = {
                    "name": self.MUX_NAME.format(mux1=entry[0], mux2=entry[1]),
                    "raw_file": self.MUX_RAW_FILE.format(mux1=entry[0], mux2=entry[1]),
                    "raw_value": 0,
                    "input_file": self.MUX_INPUT_FILE.format(mux1=entry[0], mux2=entry[1]),
                    "input_value": 0,
                    "offset": 0
                }
            else:
                channel = {
                    "name": self.NAME.format(mux1=entry),
                    "raw_file": self.RAW_FILE.format(mux1=entry),
                    "raw_value": 0,
                    "input_file": self.INPUT_FILE.format(mux1=entry),
                    "input_value": 0,
                    "offset": 0
                }

            self.__channels.append(channel)

    def __update_data(self):
        for channel in self.__channels:
            try:
                with open(channel["raw_file"],'r') as file: 
                    channel["raw_value"] = int(file.read().strip())

                with open(channel["input_file"],'r') as file: 
                    channel["input_value"] = int(file.read().strip())
            except Exception:
                print(f"PT100 could not take data from {channel['name']}")
                continue

    def get_sensor_data(self):
        self.__update_data()
        return self.__channels
