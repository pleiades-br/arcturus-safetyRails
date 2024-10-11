import threading
from dataclasses import dataclass

@dataclass
class SensorData():
    """
    Sensor data class
    """
    name: str
    hw_name: str
    raw_file: str
    raw_value: int = 0
    input_file: str
    input_vale: int = 0
    offset: int = 0

class Sensor():
    """
    Base class for the sensor board

    Args:
        Name: the sensor name/nickname 
    """
    def __init__(self, name) -> None:
        self.lock = threading.Lock()
        self.sensor_name = name
