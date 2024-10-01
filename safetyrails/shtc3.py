import os
from shared_linux_const import LINUX_SYS_I2C_PATH

class Shtc3():
    TEMPERATURE_FILE = "hwmon/hwmon0/temp1_input"
    HUMIDITY_FILE = "hwmon/hwmon0/humidity1_input"

    def __init__(self) -> None:
        self.__temperature: float = 0
        self.__humidity: float = 0
        self.__dirpath: str = ""
        self.__get_dirpath()

    def __get_dirpath(self):
        for dirs in os.listdir(LINUX_SYS_I2C_PATH):
            sensor_name_file = os.path.join(LINUX_SYS_I2C_PATH, dirs, 'name')
            if os.path.isfile(sensor_name_file):
                try:
                    with open(sensor_name_file, 'r') as file:
                        sensor_name = file.read().strip()
                        if sensor_name == 'shtc3':
                            self.__dirpath = os.path.join(LINUX_SYS_I2C_PATH, dirs)
                            break
                except Exception:
                    continue

        if self.__dirpath == "":
            raise FileNotFoundError("Could not find shtc3 sys folder")

    def __get_driver_data(self, filename):
        try:
            with open(filename, 'r') as file:
                return int(file.read().strip())

        except Exception as error:
            print(f'SHTC3 can\'t get {filename} data. Error {type(error).__name__} - {error}')
            return error

    def __update_temperature_data(self):
        value = self.__get_driver_data(os.path.join(self.__dirpath, self.TEMPERATURE_FILE))
        if isinstance(value, int):
            # Scale from linux to avoid float points"
            self.__temperature = float(value / 1000)

    def __update_humidity_data(self):
        value = self.__get_driver_data(os.path.join(self.__dirpath, self.HUMIDITY_FILE))
        if isinstance(value, int):
            # Scale from linux to avoid float points"
            self.__humidity = float(value / 1000)

    def get_sensor_data(self):
        self.__update_temperature_data()
        self.__update_humidity_data()
        return self.__temperature, self.__humidity
