import threading
from dataclasses import dataclass, asdict
import json


@dataclass
class SensorData():
    """
    Sensor data class
    """
    name: str
    hw_name: str = ""
    raw_file: str = ""
    raw_value: int = 0
    input_file: str = ""
    input_value: int = 0
    value: float = 0   # converted value
    offset: int = 0

    def to_dict(self, include: list = None) -> dict:
        """
        Convert selected attributes to a dictionary.
        """
        data_dict = asdict(self)

        # Filter the dictionary to only include specified attributes
        if include:
            data_dict = {key: data_dict[key] for key in include if key in data_dict}
        return data_dict

    def to_json(self, include: list = None) -> str:
        """
        Convert selected attributes to JSON format.
        """
        data_dict = asdict(self)

        # Filter the dictionary to only include specified attributes
        if include:
            data_dict = {key: data_dict[key] for key in include if key in data_dict}
        return json.dumps(data_dict)


class Sensor():
    """
    Base class for the sensor board

    Args:
        Name: the sensor name/nickname 
    """
    def __init__(self, name) -> None:
        self.lock = threading.Lock()
        self.sensor_name = name
