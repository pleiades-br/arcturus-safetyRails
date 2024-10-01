import os
import gpiod
from gpiod.line import Edge, Direction, Value, Bias

class ArcturusGpios():
    def __init__(self, gpio_chip, gpio_id, consumer_name) -> None:
        self.__line = None

        try:
            with gpiod.request_lines(
                path=gpio_chip,
                consumer=consumer_name,
                config={gpio_id: gpiod.LineSettings(direction=Direction.INPUT)},
            ) as line:
                self.__line = line
        except Exception as error:
            print(f'ArcturusGpio could not get {gpio_chip}:{gpio_id} for {consumer_name} \
                  Error {type(error).__name__} - {error}')
            
    def get_value(self, gpio_id):
        if self.__line != None:
            return self.__line.get_value(gpio_id)
        
        return 0
