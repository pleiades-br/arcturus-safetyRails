import threading
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
                                        'name': "Sensor Corrente de Barra",
                                        'ch1': 0,
                                        'ch2': 1,
                                    },
                                    {
                                        'name': "External Analog DC/Input J3",
                                        'ch1': 3,
                                    },
                                    {
                                        'name': "External Analog DC/Input J4",
                                        'ch1': 2,
                                    },
                               ])

        self.pac1945 = Pac1945("PAC1952",
                               [
                                    {
                                        'name': "Bateria",
                                        'ch1': 1,
                                    },
                                    {
                                        'name': "Célula Solar",
                                        'ch1': 2,                                        
                                    },
                               ])

        self.pt100 = Pt100("PT100",
                            [
                                {
                                    'name': "Temperature Sensor CH1",
                                    'ch1': 0,
                                    'ch2': 1,
                                },
                                {
                                    'name':  "Temperature Sensor CH2",
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
