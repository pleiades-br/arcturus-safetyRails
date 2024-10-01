import threading
from shtc3 import Shtc3
from pt100 import Pt100
import arcturus_gpios
import pac1945
import ads1115

class Sensors():
    def __init__(self) -> None:
        self.lock = threading.Lock()
        self.shtc3 = Shtc3()
        self.pt100 = Pt100([[0,1],[2,3]])

