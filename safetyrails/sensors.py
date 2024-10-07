import threading
from shtc3 import Shtc3
from pt100 import Pt100
from pac1945 import Pac1945
from ads1115 import Ads1115



class Sensors():
    """
    Take care off all sensor inside the arcturus board and get
    transformed information from the sensors. 

    Args:
        sensos_conf: Dictionary container the start parameters for each sensors
                     We are not checking here if the conf exist
    """
    def __init__(self, sensors_conf: dict) -> None:
        self.lock = threading.Lock()
        self.shtc3 = Shtc3()
        self.pt100 = Pt100(sensors_conf["pt100"])
        self.ads1115 = Ads1115(sensors_conf["ads1115"])
        self.pac1945 = Pac1945(sensors_conf["pac1945"])


    def __get_shtc3_data(self):
        return self.shtc3.get_sensor_data()

    def __get_pt100_data(self):
        channels = self.pt100.get_sensor_data()
        return channels

    def __get_ads1115_data(self):
        channels = self.ads1115.get_sensor_data()
        return channels

    def __get_pac1945_data(self):
        channels = self.pac1945.get_sensor_data()
        return channels

    def get_sensors_data(self):
        temp, humi = self.__get_shtc3_data()
        return {
            "shtc3": {
                "temp": temp,
                "humi": humi,
            },

            "pt100": self.__get_pt100_data(),
            "ads1115": self.__get_ads1115_data(),
            "pac1945": self.__get_pac1945_data(),
        }
