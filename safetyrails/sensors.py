import threading
import pac1945
from shtc3 import Shtc3
import arcturus_gpios
import pt100
import ads1115

class Sensors():
    def __init__(self) -> None:
        self.lock = threading.Lock()
        self.shtc3 = Shtc3()

