import os
import gpiod
from gpiod.line import Direction, Value

class HWGpio():
    """
        Create a gpio object that will monitor the gpio value
    """
    GPIO_DEV_PATH="""/dev/gpiochip{n}"""

    def __init__(self, gpio_chip, gpio_id, consumer_name) -> None:
        self.__gpio_id = gpio_id
        self.__last_value = False
        self.__gpio_chip = self.GPIO_DEV_PATH.format(n=gpio_chip)
        self.__consumer = consumer_name

    def get_value(self):
        """
            Return the current value (0 or 1) from a given gpio

        Returns:
            int: 0 or 1 for the current value
                -1 for an error
        """
        try:
            with gpiod.request_lines(
                path=self.__gpio_chip,
                consumer=self.__consumer,
                config={self.__gpio_id: gpiod.LineSettings(direction=Direction.INPUT)},
            ) as line:
                value = line.get_value(self.__gpio_id)
        except Exception as error:
            print(f'ArcturusGpio could not get {self.__gpio_chip}:{self.__gpio_id} \
                  for {self.__consumer}\n Error {type(error).__name__} - {error}')

        if value == Value.ACTIVE:
            self.__last_value = True
        else:
            self.__last_value = False

        return self.__last_value
