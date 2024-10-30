import os
from os_shared import LINUX_SYS_I2C_PATH
from sensor import Sensor, SensorData

class Shtc3(Sensor):
    """
    This class works with the data from shtc3
    Read the linux subsystem inside /sys and make all necessary
    data transformation

    Raises:
        FileNotFound: When could not find the ads122c04 inside /sys
    """

    TEMPERATURE_FILE = "hwmon/hwmon0/temp1_input"
    HUMIDITY_FILE = "hwmon/hwmon0/humidity1_input"

    def __init__(self, sensor_name: str) -> None:
        super().__init__(sensor_name)
        self.__temperature: SensorData(name="Temperature", raw_file=self.TEMPERATURE_FILE)
        self.__humidity: SensorData(name="Humidity", raw_file=self.HUMIDITY_FILE)
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
        print(self.__temperature)
        value = self.__get_driver_data(os.path.join(self.__dirpath,
                                                    getattr(self.__temperature, "raw_file")))
        if isinstance(value, int):
            # Scale from linux to avoid float points"
            setattr(self.__temperature, "raw_value", value)
            setattr(self.__temperature, "value", float(value / 1000))

    def __update_humidity_data(self):
        value = self.__get_driver_data(os.path.join(self.__dirpath, 
                                                    getattr(self.__humidity, "raw_file")))
        if isinstance(value, int):
            # Scale from linux to avoid float points"
            setattr(self.__humidity, "raw_value", value)
            setattr(self.__humidity, "value", float(value / 1000))

    def get_sensor_data(self):
        """ 
        Get an update sensor data
            
        Returns:
             float: temperature and humidity
        """
        self.__update_temperature_data()
        self.__update_humidity_data()
        return self.__temperature, self.__humidity
