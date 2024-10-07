import threading


class Sensor():
    """
    Base class for the sensor board

    Args:
        Name: the sensor name/nickname 
    """
    def __init__(self, name) -> None:
        self.lock = threading.Lock()
        self.sensor_name = name
