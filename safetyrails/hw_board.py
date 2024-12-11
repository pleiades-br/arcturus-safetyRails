import threading
import json
import os
from ads1115 import Ads1115
from pac1945 import Pac1945
from pt100 import Pt100
from shtc3 import Shtc3
from hwgpio import HWGpio



class HWBoard():
    SENSOR_DATA_PATH = "/tmp/safetyrails/"
    SENSOR_DATA_FILE = "/tmp/safetyrails/sensordata"
    """
        This is the HWBoard for the sense Arcturus
        Containing all the sensors and gpios that need to watch
        for the main application 
    """
    def __init__(self) -> None:
        self.ads1115 = Ads1115("ADS1115",
                               [
                                    {
                                        'name': "vcc_bar",
                                        'ch1': 0,
                                        'ch2': 1,
                                    },
                                    {
                                        'name':"input_j3",
                                        'ch1': 3,
                                    },
                                    {
                                        'name': "input_j4",
                                        'ch1': 2,
                                    },
                               ])

        self.pac1945 = Pac1945("PAC1952",
                               [
                                    {
                                        'name': "battery",
                                        'ch1': 1,
                                    },
                                    {
                                        'name': "solar_cel",
                                        'ch1': 4,                                        
                                    },
                               ])

        self.pt100 = Pt100("PT100",
                            [
                                {
                                    'name': "temperature_bar_ch1",
                                    'ch1': 1,
                                    'ch2': 0,
                                },
                            ])

        self.shtc3 = Shtc3("SHTC3")
        self.gpio_lock = threading.Lock()
        self.barra_in = HWGpio(3, 20, "BAR IN")
        self.is_barra_in_alarm_sent = False
        self.pta1 = HWGpio(4, 6, "PTA1")
        self.pta2 = HWGpio(4, 4, "PTA2")
        self.__update_all_sensors()
        try:
            os.mkdir(self.SENSOR_DATA_PATH)
        except Exception as e:
            print(f"An error occurred: {e}")

    def __update_all_sensors(self):
        """
        Force a sensor reading on all sensors available on Hwboard
        """
        self.shtc3.update_sensor_data()
        self.ads1115.update_sensor_data()
        self.pt100.update_sensor_data()
        self.pac1945.update_sensor_data()

    def get_all_sensors_values_as_json(self) -> str:
        """
        Get all sensors value and return as json format
        Returns:
            str: all sensors in json format
        """
        temperature_hw, humidity_hw = self.shtc3.get_sensor_data()

        sensors_data = {
            'temp_hw': temperature_hw.value,
            'humi_hw': humidity_hw.value,
            'vcc_bar_sensor': self.ads1115.get_sensor_value_as_dict(),
            'temp_bar_sensor': self.pt100.get_sensor_raw_value_as_dict(),
            'power_supply': self.pac1945.get_sensor_value_as_dict(),
            'external_alarms': {
                'bar_in': self.barra_in.get_value(),
                'pta1': self.pta1.get_value(),
                'pta2': self.pta2.get_value()
            }
        }

        return json.dumps(sensors_data)
    
    def save_data_to_sensor_tmp_file(self):
        try:
            with open(self.SENSOR_DATA_FILE, 'w') as json_file:
                sensor_data = self.get_all_sensors_values_as_json()
                json.dump(sensor_data, json_file)
        except Exception as e:
            print(f"Not possible to save sensor data on tmp file: {e}")
