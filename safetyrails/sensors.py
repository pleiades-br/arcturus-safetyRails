import threading
from shtc3 import Shtc3
from pt100 import Pt100
from pac1945 import Pac1945
from ads1115 import Ads1115
import arcturus_gpios


class Sensors():
    def __init__(self) -> None:
        self.lock = threading.Lock()
        self.shtc3 = Shtc3()
        self.pt100 = Pt100([[0,1],[2,3]])
        self.ads1115 = Ads1115(0,1,2,3)
        self.pac1945 = Pac1945([1,2])

