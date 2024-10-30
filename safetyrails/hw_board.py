import threading
import json
from ads1115 import Ads1115
from pac1945 import Pac1945
from pt100 import Pt100
from shtc3 import Shtc3
from hwgpio import HWGpio



class HWBoard():
    """
        This is the HWBoard for the sense Arcturus
        Containing all the sensors and gpios that need to watch
        for the main application 
    """
    def __init__(self) -> None:
        self.ads1115 = Ads1115("ADS1115",
                               [
                                    {
                                        'name': "corrent_barra",
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
                                        'name': "bateria",
                                        'ch1': 1,
                                    },
                                    {
                                        'name': "celula_solar",
                                        'ch1': 2,                                        
                                    },
                               ])

        self.pt100 = Pt100("PT100",
                            [
                                {
                                    'name': "temperature_rail_ch1",
                                    'ch1': 0,
                                    'ch2': 1,
                                },
                                {
                                    'name':  "temperature_rail_ch2",
                                    'ch1': 2,
                                    'ch2': 3,
                                }
                            ])

        self.shtc3 = Shtc3("SHTC3")
        self.gpio_lock = threading.Lock()
        self.barra_in = HWGpio(3, 20, "Rail Bar")
        self.is_barra_in_alarm_sent = False
        self.pta1 = HWGpio(4, 6, "PTA1")
        self.pta2 = HWGpio(4, 4, "PTA2")

    def sensors_values_to_json(self) -> str:
        """
        Get all sensors value and return in a json format
        Returns:
            str: all sensors in json format
        """
        temperature_hw, humidity_hw = self.shtc3.get_sensor_data()
        ads_channels = self.ads1115.get_sensor_data()
        pta_channels = self.pt100.get_sensor_data()
        pac_channels = self.pac1945.get_sensor_data()

        sensors_data = {
            "temp_hw": temperature_hw.to_json("value"),
            "humi_hw": humidity_hw.to_json("value"),
            "external_sensors": {
                [channel.to_dict_name_raw_value() for channel in ads_channels],
                [channel.to_dict_name_raw_value() for channel in pta_channels],
                [channel.to_to_dict_name_raw_value() for channel in pac_channels]
            },
            "external_alarms": {
                "barra_in": self.barra_in.get_value(),
                "pta1": self.pta1.get_value(),
                "pta2": self.pta2.get_value()
            }
        }

        return json.dumps(sensors_data)
