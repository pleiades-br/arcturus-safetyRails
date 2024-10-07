import os
import gpiod
from gpiod.line import Edge, Direction, Value, Bias

class ArcturusGpios():
    """
        Create a gpio object that will monitor the gpio value
    """
    GPIO_DEV_PATH="""/dev/gpiochip{gpio_chip}"""

    def __init__(self, gpio_chip, gpio_id, consumer_name) -> None:
        self.__line = None

        try:
            with gpiod.request_lines(
                path=self.GPIO_DEV_PATH.format(gpio_chip),
                consumer=consumer_name,
                config={gpio_id: gpiod.LineSettings(direction=Direction.INPUT)},
            ) as line:
                self.__line = line
        except Exception as error:
            print(f'ArcturusGpio could not get {gpio_chip}:{gpio_id} for {consumer_name} \
                  Error {type(error).__name__} - {error}')

    def get_value(self, gpio_id):
        """
            Return the current value (0 or 1) from a given gpio
        Args:
            gpio_id (int): the gpio_id 

        Returns:
            int: 0 or 1 for the current value
                -1 for an error
        """
        if self.__line is not None:
            return self.__line.get_value(gpio_id)

        return -1
